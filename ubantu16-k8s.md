deb https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main



```js
# Debian/Ubuntu
apt-get update && apt-get install -y apt-transport-https
curl -s https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg | apt-key add -
cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main
EOF
apt-get update
apt-get install -y kubelet kubeadm kubectl

# CentOS/RHEL/Fedora
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF
setenforce 0
yum install -y kubelet kubeadm kubectl
```



```
kubeadm init --kubernetes-version=1.15.0 \

--apiserver-advertise-address=192.168.12.136 \

--image-repository registry.aliyuncs.com/google_containers \

--service-cidr=10.1.0.0/16 \

--pod-network-cidr=10.244.0.0/16
```



kubectl create clusterrolebinding system-node-role-bound --clusterrole=system:node --group=system:nodes



\#（1）临时关闭swap分区, 重启失效; 
swapoff -a

\#（2）永久关闭swap分区

sed -ri 's/.*swap.*/#&/' /etc/fstab

https://blog.51cto.com/6923450605400/735323





# 1.k8s kubeadm 搭建

## 环境

ubantu

vmware, unbantu16,



## 配置源

apt-get update && apt-get install -y apt-transport-https
curl -s https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg | apt-key add -
cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main
EOF
apt-get update
apt-get install -y kubelet kubeadm kubectl



## kubeadm init

https://kubernetes.io/zh/docs/reference/setup-tools/kubeadm/kubeadm-init/



出现问题：

#（1）临时关闭swap分区, 重启失效; 
swapoff -a

\#（2）永久关闭swap分区

sed -ri 's/.*swap.*/#&/' /etc/fstab

https://blog.51cto.com/6923450605400/735323



```
[root@master]# kubectl get pod
The connection to the server localhost:8080 was refused - did you specify the right host or port?
```

出现这个问题的原因是kubectl命令需要使用kubernetes-admin来运行，解决方法如下，将主节点中的【/etc/kubernetes/admin.conf】文件拷贝到从节点相同目录下，然后配置环境变量：

```
echo "export KUBECONFIG=/etc/kubernetes/admin.conf" >> ~/.bash_profile
source ~/.bash_profile
```



## 网络

https://kubernetes.io/zh/docs/concepts/cluster-administration/addons/



## 可视化管理

https://github.com/kubernetes/dashboard/wiki/Creating-sample-user



## 为特定的ClusterRole创建ClusterRoleBinding。

http://docs.kubernetes.org.cn/494.html 





