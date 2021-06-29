typedef struct {
	char topic[64];
	int16_t topic_len;
	int32_t canid;
	int16_t ext;
	int16_t rtr;
	int16_t data_len;
	char data[8];
} FRAME_t;

typedef struct {
    uint16_t frame;
    uint32_t canid;
    char * topic;
	int16_t topic_len;
} TOPIC_t;

