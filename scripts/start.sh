#!/usr/bin/env bash

set -eux

function set_yaml_prop() {
    local target_file="${1}"
    local key="${2}"
    local value="${3}"

    /usr/bin/python3 /usr/bin/set_conf.py --file "${target_file}" --key "${key}" --value "${value}"
}

CLUSTER_NAME="${CLUSTER_NAME:-test-cassandra-claster}"
NODE_HOST="${NODE_HOST:-localhost}"
SEED_HOSTS="${SEED_HOSTS:-127.0.0.1:7000}"
ENDPOINT_SNITCH="${ENDPOINT_SNITCH:-SimpleSnitch}"

cassandra_yaml="${CASSANDRA_CONF}/cassandra.yaml"
set_yaml_prop "${cassandra_yaml}" "cluster_name" "${CLUSTER_NAME}"
set_yaml_prop "${cassandra_yaml}" "listen_address" "${NODE_HOST}"
# TODO. seeds may be set incorectly if many is provided
set_yaml_prop "${cassandra_yaml}" "seed_provider.0.parameters.0.seeds" "${SEED_HOSTS}"
set_yaml_prop "${cassandra_yaml}" "endpoint_snitch" "${ENDPOINT_SNITCH}"


set_yaml_prop "${CASSANDRA_CONF}/cassandra.yaml" "hints_directory" "${CASSANDRA_HINTS_DIR}"
set_yaml_prop "${CASSANDRA_CONF}/cassandra.yaml" "data_file_directories" "[\"${CASSANDRA_DATA_DIR}\"]"
set_yaml_prop "${CASSANDRA_CONF}/cassandra.yaml" "commitlog_directory" "${CASSANDRA_COMMIT_LOG_DIR}"
set_yaml_prop "${CASSANDRA_CONF}/cassandra.yaml" "saved_caches_directory" "${CASSANDRA_SAVED_CACHES_DIR}"

exec "${CASSANDRA_BIN}"/cassandra -f

