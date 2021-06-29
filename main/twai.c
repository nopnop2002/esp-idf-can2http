/* TWAI Network Example

   This example code is in the Public Domain (or CC0 licensed, at your option.)

   Unless required by applicable law or agreed to in writing, this
   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
   CONDITIONS OF ANY KIND, either express or implied.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "freertos/semphr.h"
#include "esp_err.h"
#include "esp_log.h"
#include "driver/twai.h" // Update from V4.2

#include "twai.h"

static const char *TAG = "TWAI";

extern QueueHandle_t xQueue_http;
//extern QueueHandle_t xQueue_twai_tx;

extern TOPIC_t *publish;
extern int16_t npublish;

void dump_table(TOPIC_t *topics, int16_t ntopic);

void twai_task(void *pvParameters)
{
	ESP_LOGI(TAG,"task start");
	dump_table(publish, npublish);

	twai_message_t rx_msg;
	FRAME_t frameBuf;
	while (1) {
		esp_err_t ret = twai_receive(&rx_msg, pdMS_TO_TICKS(1));
		if (ret == ESP_OK) {
			ESP_LOGD(TAG,"twai_receive identifier=0x%x flags=0x%x data_length_code=%d",
				rx_msg.identifier, rx_msg.flags, rx_msg.data_length_code);

			int ext = rx_msg.flags & 0x01;
			int rtr = rx_msg.flags & 0x02;
			ESP_LOGD(TAG, "ext=%x rtr=%x", ext, rtr);

#if CONFIG_ENABLE_PRINT
			if (ext == 0) {
				printf("Standard ID: 0x%03x     ", rx_msg.identifier);
			} else {
				printf("Extended ID: 0x%08x", rx_msg.identifier);
			}
			printf(" DLC: %d  Data: ", rx_msg.data_length_code);

			if (rtr == 0) {
				for (int i = 0; i < rx_msg.data_length_code; i++) {
					printf("0x%02x ", rx_msg.data[i]);
				}
			} else {
				printf("REMOTE REQUEST FRAME");

			}
			printf("\n");
#endif

			for(int index=0;index<npublish;index++) {
				if (publish[index].frame != ext) continue;
				if (publish[index].canid == rx_msg.identifier) {
					ESP_LOGI(TAG, "publish[%d] frame=%d canid=0x%x topic=[%s] topic_len=%d",
					index, publish[index].frame, publish[index].canid, publish[index].topic, publish[index].topic_len);
					strcpy(frameBuf.topic, publish[index].topic);
					frameBuf.topic_len = publish[index].topic_len;
					frameBuf.canid = rx_msg.identifier;
					frameBuf.ext = ext;
					frameBuf.rtr = rtr;
					if (rtr == 0) {
						frameBuf.data_len = rx_msg.data_length_code;
					} else {
						frameBuf.data_len = 0;
					}
					for(int i=0;i<frameBuf.data_len;i++) {
						frameBuf.data[i] = rx_msg.data[i];
					}
					if (xQueueSend(xQueue_http, &frameBuf, portMAX_DELAY) != pdPASS) {
						ESP_LOGE(TAG, "xQueueSend Fail");
					}
				}
			}

		} else if (ret == ESP_ERR_TIMEOUT) {

		} else {
			ESP_LOGE(TAG, "twai_receive Fail %s", esp_err_to_name(ret));
		}
	}

	// never reach
	vTaskDelete(NULL);
}

