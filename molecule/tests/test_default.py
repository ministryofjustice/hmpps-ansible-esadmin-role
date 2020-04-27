import os

import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_docker_is_installed(host):
    docker = host.package('docker-ce')
    assert docker.is_installed


def test_docker_running_and_enabled(host):
    docker = host.service("docker")
    assert docker.is_running
    assert docker.is_enabled
    assert host.socket("tcp://0.0.0.0:2376").is_listening


@pytest.mark.parametrize(
    "dir",
    [
        '/opt/docker/data',
        '/etc/docker',
        '/etc/docker/certs',
        '/etc/systemd/system/docker.service.d',
        '/opt/eslocal',
        '/opt/scripts'
    ]
)
def test_docker_directories_exist(host, dir):
    assert host.file(dir).is_directory


@pytest.mark.parametrize(
    "dfile",
    [
        '/etc/docker/daemon.json',
        '/etc/docker/certs/ca.pem',
        '/etc/docker/certs/cert.pem',
        '/etc/docker/certs/key.pem',
        '/etc/systemd/system/docker.service.d/docker.conf',
        '/bin/docker-compose',
        '/opt/docker-compose.yml',
        '/opt/storage-sync.sh'
    ]
)
def test_docker_config_files_exist(host, dfile):
    assert host.file(dfile).is_file
    assert host.file(dfile).exists


@pytest.mark.parametrize(
    "grp",
    [
        'docker',
        'elasticsearch'
    ]
)
def test_system_groups_exists(host, grp):
    assert host.group(grp).exists


@pytest.mark.parametrize(
    "usr",
    [
        'elasticsearch'
    ]
)
def test_system_users_exists(host, usr):
    assert host.user(usr).exists
