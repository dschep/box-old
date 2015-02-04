# An Ansible config for setting up a computer to my tastes

## bootstrap

```
sudo apt-get install software-properties-common
sudo apt-add-repository ppa:ansible/ansible
sudo apt-get update
sudo apt-get install ansible git
git clone https://github.com/dschep/box.git
cd box
./run
```
