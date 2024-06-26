project(${CMAKE_PROJECT_NAME}-protos)

find_package(Protobuf CONFIG REQUIRED)

set (PROTO_FILES
	${CMAKE_CURRENT_SOURCE_DIR}/grsim/grSim_Commands.proto
	${CMAKE_CURRENT_SOURCE_DIR}/grsim/grSim_Packet.proto
	${CMAKE_CURRENT_SOURCE_DIR}/grsim/grSim_Replacement.proto
	${CMAKE_CURRENT_SOURCE_DIR}/grsim/grSim_Robotstatus.proto
	${CMAKE_CURRENT_SOURCE_DIR}/immortals/data_plot.proto
	${CMAKE_CURRENT_SOURCE_DIR}/immortals/Imm_wrapper.proto
	${CMAKE_CURRENT_SOURCE_DIR}/immortals/micro.proto
	${CMAKE_CURRENT_SOURCE_DIR}/immortals/robot_control.proto
	${CMAKE_CURRENT_SOURCE_DIR}/immortals/robot_feedback.proto
	${CMAKE_CURRENT_SOURCE_DIR}/immortals/strategy.proto
	${CMAKE_CURRENT_SOURCE_DIR}/immortals/text_log.proto
	${CMAKE_CURRENT_SOURCE_DIR}/immortals/vision_interface.proto
	${CMAKE_CURRENT_SOURCE_DIR}/immortals/visual_log.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-game-controller/ssl_autoref_ci.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-game-controller/ssl_gc_api.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-game-controller/ssl_gc_change.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-game-controller/ssl_gc_ci.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-game-controller/ssl_gc_common.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-game-controller/ssl_gc_engine.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-game-controller/ssl_gc_engine_config.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-game-controller/ssl_gc_game_event.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-game-controller/ssl_gc_geometry.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-game-controller/ssl_gc_rcon.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-game-controller/ssl_gc_rcon_autoref.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-game-controller/ssl_gc_rcon_remotecontrol.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-game-controller/ssl_gc_rcon_team.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-game-controller/ssl_gc_referee_message.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-game-controller/ssl_gc_state.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-refbox/game_event.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-refbox/referee.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-simulation-protocol/ssl_simulation_config.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-simulation-protocol/ssl_simulation_control.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-simulation-protocol/ssl_simulation_error.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-simulation-protocol/ssl_simulation_robot_control.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-simulation-protocol/ssl_simulation_robot_feedback.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-simulation-protocol/ssl_simulation_synchronous.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-simulation-protocol/erforce/ssl_simulation_custom_erforce_realism.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-simulation-protocol/erforce/ssl_simulation_custom_erforce_robot_spec.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-vision/messages_robocup_ssl_detection.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-vision/messages_robocup_ssl_detection_tracked.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-vision/messages_robocup_ssl_geometry.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-vision/messages_robocup_ssl_geometry_legacy.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-vision/messages_robocup_ssl_refbox_log.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-vision/messages_robocup_ssl_wrapper.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-vision/messages_robocup_ssl_wrapper_legacy.proto
	${CMAKE_CURRENT_SOURCE_DIR}/ssl-vision/messages_robocup_ssl_wrapper_tracked.proto)

	
set (NANO_PROTO_FILES
	${CMAKE_CURRENT_SOURCE_DIR}/immortals/micro.proto)

set(PROTO_SRCS)
set(PROTO_HDRS)

set(PROTO_DEF_BASE_DIR ${CMAKE_CURRENT_SOURCE_DIR})
set(PROTO_GEN_BASE_DIR ${CMAKE_CURRENT_BINARY_DIR})

foreach(file ${PROTO_FILES})
	get_filename_component(FILE_ABS ${file} ABSOLUTE)  # Full path to file
	get_filename_component(FILE_WE  ${file} NAME_WE)   # File name with neither the directory nor the longest extension
	get_filename_component(FILE_DIR ${file} DIRECTORY) # Directory without file name

	file(RELATIVE_PATH FILE_REL     ${PROTO_DEF_BASE_DIR} ${FILE_ABS})
	file(RELATIVE_PATH FILE_DIR_REL ${PROTO_DEF_BASE_DIR} ${FILE_DIR})

	set(GEN_DIR "${PROTO_GEN_BASE_DIR}/${FILE_DIR_REL}")
	set(GEN_FILE_HEADER "${GEN_DIR}/${FILE_WE}.pb.h")
	set(GEN_FILE_SOURCE "${GEN_DIR}/${FILE_WE}.pb.cc")

	list(APPEND PROTO_SRCS ${GEN_FILE_SOURCE})
	list(APPEND PROTO_HDRS ${GEN_FILE_HEADER})

	add_custom_command(
	OUTPUT ${GEN_FILE_SOURCE}
			${GEN_FILE_HEADER}
	COMMAND  ${PROTOBUF_PROTOC_EXECUTABLE}
	ARGS --proto_path=${PROTO_DEF_BASE_DIR} --cpp_out=${PROTO_GEN_BASE_DIR} ${FILE_REL} 
	DEPENDS ${FILE_ABS}
	COMMENT "Running C++ protocol buffer compiler on ${FILE_REL}"
	VERBATIM )
endforeach()

add_library(${PROJECT_NAME}
    ${PROTO_SRCS} ${PROTO_HDRS}
    ${PROTO_FILES})

target_include_directories(${PROJECT_NAME} PUBLIC "${CMAKE_CURRENT_BINARY_DIR}")

source_group(TREE ${CMAKE_CURRENT_SOURCE_DIR} FILES ${PROTO_FILES})
source_group(TREE ${CMAKE_CURRENT_BINARY_DIR} PREFIX "generated" FILES ${PROTO_SRCS} ${PROTO_HDRS})

target_link_libraries(${PROJECT_NAME} PUBLIC
    protobuf::libprotobuf)

set_target_properties(${PROJECT_NAME} PROPERTIES UNITY_BUILD OFF)

target_precompile_headers(${PROJECT_NAME} 
	INTERFACE ${PROTO_HDRS})
