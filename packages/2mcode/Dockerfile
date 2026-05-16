FROM alpine AS base

# Disable the runtime transpiler cache by default inside Docker containers.
# On ephemeral containers, the cache is not useful
ARG BUN_RUNTIME_TRANSPILER_CACHE_PATH=0
ENV BUN_RUNTIME_TRANSPILER_CACHE_PATH=${BUN_RUNTIME_TRANSPILER_CACHE_PATH}
RUN apk add libgcc libstdc++ ripgrep

FROM base AS build-amd64
COPY dist/2M_CODE-linux-x64-baseline-musl/bin/2M_CODE /usr/local/bin/2M_CODE

FROM base AS build-arm64
COPY dist/2M_CODE-linux-arm64-musl/bin/2M_CODE /usr/local/bin/2M_CODE

ARG TARGETARCH
FROM build-${TARGETARCH}
RUN 2M_CODE --version
ENTRYPOINT ["2M_CODE"]
