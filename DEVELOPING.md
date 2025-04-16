## Setting up a local development environment

Setup instructions should work for both Docker (tested on a Mac with Docker Desktop)
and (rootless) Podman.

### Install prerequisites

- [gitlab-ci-local](https://github.com/firecow/gitlab-ci-local).
- Podman or Docker
- GNU Make
- `qemu-user-static` to enable cros-platform builds on Linux.

### Set up a container network for builds

To run CI jobs locally, a container network with DNS for container names enabled
is necessary. The default network has it disabled, so not suitable.
To create a new network named `localci` run

```shell
docker network create localci
```

### Set up a local container registry

Container builds need a registry to store and pass built images between jobs.
To start a local registry container named `localci-registry` in background run

```
docker run -d --restart=on-failure -p 5001:5000 --name localci-registry --network localci \
    docker.io/library/registry:2
```

### Define local CI variables

Use the following example to create `.gitlab-ci-local-variables.yml`. Note
the `localci-registry` address matching the name of the local registry container
created earlier.

```shell
{
    read -rp 'DockerHub username: ' dockerhub_user
    read -rsp 'DockerHub token: ' dockerhub_token
    read -rsp 'PyPI token' pypi_token
    dockerhub_auth=$(printf '%s:%s' "$dockerhub_user" "$dockerhub_token" | base64)

    cat <<EOF >.gitlab-ci-local-variables.yml
---
CI_REGISTRY: 'localci-registry:5000'
CI_REGISTRY_IMAGE: 'localci-registry:5000/${CI_PROJECT_PATH}'
TRIVY_INSECURE: 'true'
CONTAINERS_REGISTRIES_CONF:
  type: file
  values:
    '*': |
      [[registry]]
      location = "localci-registry:5000"
      insecure = true

REGISTRY_AUTH_FILE:
  type: file
  values:
    '*': |
      {"auths": {
        "docker.io": {
          "auth": "${dockerhub_auth}"
        }
      }}
POETRY_PYPI_TOKEN_PYPI: "${pypi_token}"
EOF
}
```

## Running builds locally

Run `make pipeline` to run the pipeline defined in [.gitlab-ci.yml](.gitlab-ci.yml).
Run `make publish-pipeline` to run the pipeline including the manual `publish` job.

See [Makefile](Makefile) for more details. Override `CONTAINER_NETWORK` if the
default `localci` is different from the network name created earlier.

## Local tasks

- `make reformat` automatically re-formats the Python code and sorts imports.

See `.local-tasks.yml` for more information.

## Releasing

- Remove the `.devN` version identifier in [pyproject.toml](pyproject.toml)
  and commit the change.
- Create an annotated (to track the release date) Git tag using `vX.Y.Z` format.
  `X.Y.Z` must match the version in [pyproject.toml](pyproject.toml).
- Push the tag.
- Ensure the Git working tree is clean.
- Run `make tag-pipeline`.
- Increment the version number in [pyproject.toml](pyproject.toml) adding the `.dev0`
  identifier, and commit the change.
