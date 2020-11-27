#!/usr/bin/env bash

function install_docker() {
  # docker
  yum install -yq yum-utils
  yum-config-manager \
    --add-repo \
      https://download.docker.com/linux/centos/docker-ce.repo
  
  yum install -yq \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    # the docker daemon actually fails to start if iptables isn't installed
    iptables
 
  systemctl start docker
  systemctl enable docker
}


function install_docker_compose() {
  curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  chmod +x /usr/local/bin/docker-compose
}


function install_fail2ban() {
  yum install epel-release -yq
  yum install fail2ban -yq
  systemctl enable fail2ban

  local conf="/etc/fail2ban/jail.local"
  cat /dev/null > ${conf}
  echo "[DEFAULT]" >> ${conf}
  echo "bantime = 3600" >> ${conf}
  echo "banaction = iptables-multiport" >> ${conf}
  echo "[sshd]" >> ${conf}
  echo "enabled = true" >> ${conf}

  systemctl restart fail2ban
}


function deps() {
  yum install -yq  \
    git \
    tmux \ # to make admin easier
    httpd-tools
  
  install_docker
  install_docker_compose
}


function clone_and_build() {
  project_dir="/opt/repp"
  echo "Cleaning target project dir" 
  rm -rf ${project_dir}
  mkdir ${project_dir} -p
  cd ${project_dir}
  git clone https://github.com/LoveShack-Inc/represent.git
  cd represent
  docker build . -t repp
}


function main() {
  deps
  clone_and_build
}

main
