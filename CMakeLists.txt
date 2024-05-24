cmake_minimum_required(VERSION 3.25)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_C_STANDARD 17)
set(CMAKE_C_STANDARD_REQUIRED ON)

option(TRACE_BUILD_TIME "Use -ftime-trace to generate build time trace" OFF)
option(ENABLE_SANITIZERS "Enable address and undefined behavior sanitizers" OFF)

project(immortals-protos)

include(GNUInstallDirs)

# Enable ASAN
add_compile_options($<$<BOOL:${ENABLE_SANITIZERS}>:-fsanitize=address>)
add_link_options($<$<BOOL:${ENABLE_SANITIZERS}>:-fsanitize=address>)

if (${TRACE_BUILD_TIME})
    add_compile_options(-ftime-trace)
endif ()

find_package(Protobuf CONFIG REQUIRED)

set(PROTO_FILES
        ${CMAKE_CURRENT_SOURCE_DIR}/grsim/grsim_commands.proto
        ${CMAKE_CURRENT_SOURCE_DIR}/grsim/grsim_packet.proto
        ${CMAKE_CURRENT_SOURCE_DIR}/grsim/grsim_replacement.proto
        ${CMAKE_CURRENT_SOURCE_DIR}/grsim/grsim_robotstatus.proto
        ${CMAKE_CURRENT_SOURCE_DIR}/immortals/command.proto
        ${CMAKE_CURRENT_SOURCE_DIR}/immortals/common.proto
        ${CMAKE_CURRENT_SOURCE_DIR}/immortals/debug.proto
        ${CMAKE_CURRENT_SOURCE_DIR}/immortals/micro.proto
        ${CMAKE_CURRENT_SOURCE_DIR}/immortals/play_book.proto
        ${CMAKE_CURRENT_SOURCE_DIR}/immortals/state.proto
        ${CMAKE_CURRENT_SOURCE_DIR}/ssl-common/ssl_common.proto
        ${CMAKE_CURRENT_SOURCE_DIR}/ssl-common/ssl_geometry.proto
        ${CMAKE_CURRENT_SOURCE_DIR}/ssl-game-controller/ssl_gc_game_event.proto
        ${CMAKE_CURRENT_SOURCE_DIR}/ssl-game-controller/ssl_gc_rcon.proto
        ${CMAKE_CURRENT_SOURCE_DIR}/ssl-game-controller/ssl_gc_rcon_team.proto
        ${CMAKE_CURRENT_SOURCE_DIR}/ssl-game-controller/ssl_gc_referee_message.proto
        ${CMAKE_CURRENT_SOURCE_DIR}/ssl-simulation-protocol/ssl_simulation_config.proto
        ${CMAKE_CURRENT_SOURCE_DIR}/ssl-simulation-protocol/ssl_simulation_control.proto
        ${CMAKE_CURRENT_SOURCE_DIR}/ssl-simulation-protocol/ssl_simulation_error.proto
        ${CMAKE_CURRENT_SOURCE_DIR}/ssl-simulation-protocol/ssl_simulation_robot_control.proto
        ${CMAKE_CURRENT_SOURCE_DIR}/ssl-simulation-protocol/ssl_simulation_robot_feedback.proto
        ${CMAKE_CURRENT_SOURCE_DIR}/ssl-simulation-protocol/ssl_simulation_synchronous.proto
        ${CMAKE_CURRENT_SOURCE_DIR}/ssl-vision/messages_robocup_ssl_detection.proto
        ${CMAKE_CURRENT_SOURCE_DIR}/ssl-vision/messages_robocup_ssl_detection_tracked.proto
        ${CMAKE_CURRENT_SOURCE_DIR}/ssl-vision/messages_robocup_ssl_geometry.proto
        ${CMAKE_CURRENT_SOURCE_DIR}/ssl-vision/messages_robocup_ssl_wrapper.proto
        ${CMAKE_CURRENT_SOURCE_DIR}/ssl-vision/messages_robocup_ssl_wrapper_tracked.proto)

set(NANO_PROTO_FILES
        ${CMAKE_CURRENT_SOURCE_DIR}/immortals/micro.proto)

set(PROTO_SRCS)
set(PROTO_HDRS)

set(PROTO_DEF_BASE_DIR ${CMAKE_CURRENT_SOURCE_DIR})
set(PROTO_GEN_BASE_DIR ${CMAKE_CURRENT_BINARY_DIR})

foreach (file ${PROTO_FILES})
    get_filename_component(FILE_ABS ${file} ABSOLUTE) # Full path to file
    get_filename_component(FILE_WE ${file} NAME_WE) # File name with neither the directory nor the longest extension
    get_filename_component(FILE_DIR ${file} DIRECTORY) # Directory without file name

    file(RELATIVE_PATH FILE_REL ${PROTO_DEF_BASE_DIR} ${FILE_ABS})
    file(RELATIVE_PATH FILE_DIR_REL ${PROTO_DEF_BASE_DIR} ${FILE_DIR})

    set(GEN_DIR "${PROTO_GEN_BASE_DIR}/${FILE_DIR_REL}")
    set(GEN_FILE_HEADER "${GEN_DIR}/${FILE_WE}.pb.h")
    set(GEN_FILE_SOURCE "${GEN_DIR}/${FILE_WE}.pb.cc")

    list(APPEND PROTO_SRCS ${GEN_FILE_SOURCE})
    list(APPEND PROTO_HDRS ${GEN_FILE_HEADER})

    add_custom_command(
            OUTPUT ${GEN_FILE_SOURCE}
            ${GEN_FILE_HEADER}
            COMMAND ${PROTOBUF_PROTOC_EXECUTABLE}
            ARGS --proto_path=${PROTO_DEF_BASE_DIR} --cpp_out=${PROTO_GEN_BASE_DIR} ${FILE_REL}
            DEPENDS ${FILE_ABS}
            COMMENT "Running C++ protocol buffer compiler on ${FILE_REL}"
            VERBATIM)
endforeach ()

add_library(${PROJECT_NAME}
        ${PROTO_SRCS} ${PROTO_HDRS}
        ${PROTO_FILES})

set_target_properties(${PROJECT_NAME} PROPERTIES PUBLIC_HEADER "${PROTO_HDRS}")
target_include_directories(${PROJECT_NAME} PRIVATE "${CMAKE_CURRENT_BINARY_DIR}")

target_link_libraries(${PROJECT_NAME} PUBLIC
        protobuf::libprotobuf)

install(
        TARGETS ${PROJECT_NAME}
        EXPORT ${PROJECT_NAME})

install(EXPORT ${PROJECT_NAME} FILE ${PROJECT_NAME}-targets.cmake NAMESPACE immortals:: DESTINATION share/${PROJECT_NAME})
