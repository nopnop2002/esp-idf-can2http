set(srcs "main.c" "http_post.c" "http_server.c")

if (IDF_VERSION_MAJOR STREQUAL "5")
	list(APPEND srcs "twai_task_v5.c")
elseif (IDF_VERSION_MAJOR STREQUAL "6")
	list(APPEND srcs "twai_task_v6.c")
endif()

idf_component_register(SRCS ${srcs} INCLUDE_DIRS ".")
