#define STANDARD_FRAME 0
#define EXTENDED_FRAME 1

#define DATA_FRAME     0
#define REMOTE_FRAME   1

#define	CMD_RECEIVE	100
#define	CMD_SEND    200

typedef struct {
	int16_t command;
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

