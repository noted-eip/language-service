#!/bin/bash

# Variable definition and init
SERVICE_NAME="recommendations"
PROTOC_TOOL="python -m grpc_tools.protoc" # Could be hardcoded in CMD later on
GRPC_FOLDER="./grpc"

(
# Clean up old files
rm -rf "${GRPC_FOLDER}/${SERVICE_NAME}pb" "${SERVICE_NAME}pb" && \

# Generate protobufs files in the right folder
$PROTOC_TOOL --python_out="${GRPC_FOLDER}" --grpc_python_out="${GRPC_FOLDER}" "${GRPC_FOLDER#./}/protos/${SERVICE_NAME}/"*.proto --proto_path="${GRPC_FOLDER}/protos" && \

# Create __init__.py to easily import python files
touch "${GRPC_FOLDER}/${SERVICE_NAME}/__init__.py" && \

# Rename the folder to keep Noted's convention
mv "${GRPC_FOLDER}/${SERVICE_NAME}" "${GRPC_FOLDER}/${SERVICE_NAME}pb" && \

# Create symbolic link for easier import in Python
ln -s "${GRPC_FOLDER}/${SERVICE_NAME}pb" "${SERVICE_NAME}pb"

# Hotfix for renaming python generated package
sed -i "s/from ${SERVICE_NAME}/from ${SERVICE_NAME}pb/g" "${SERVICE_NAME}pb/${SERVICE_NAME}_pb2_grpc.py"
) \
|| echo -ne "\nGenerating protobuf files failed."