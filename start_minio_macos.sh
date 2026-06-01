#!/bin/bash

brew install minio/stable/minio
mkdir ~/minio_data
export MINIO_ROOT_USER=minioadmin
export MINIO_ROOT_PASSWORD=minioadmin

minio server ~/minio_data --console-address ":9001"
