import os
cmd = "sudo which java"
returned_value = os.system(cmd)
if returned_value ==256:
    cmd = "sudo add-apt-repository ppa:webupd8team/java"
    os.system(cmd)
    cmd = "sudo apt-get update"
    os.system(cmd)
    cmd = "sudo apt-get install oracle-java8-installer"
    os.system(cmd)
    cmd = "java -version"
    os.system(cmd)
    
    with open("~/.bashrc", "a") as myfile:
        myfile.write("\n\n")
        myfile.write("\nexport JAVA_HOME=/usr/lib/jvm/java-8-oracle")

elif returned_value == 0:
    cmd = "sudo $JAVA_HOME"
    returned_value =  os.system(cmd)
    if returned_value == 0:
	flag = 0
        print("Please set JAVA_HOME in bashrc file and then run this script again")

    
   
#cmd = 'ssh-keygen -t rsa -P ""'
#os.system(cmd)
#cmd = "cat $HOME/.ssh/id_rsa.pub >> $HOME/.ssh/authorized_keys"
#os.system(cmd)

cmd = "cd Downloads"
os.system(cmd)
if not os.path.isfile("hadoop-2.7.0.tar.gz"):
    cmd = "wget https://archive.apache.org/dist/hadoop/core/hadoop-2.7.0/hadoop-2.7.0.tar.gz"
    os.system(cmd)

cmd = "sudo tar -xzvf hadoop-2.7.0.tar.gz" 
os.system(cmd)



cmd = "sudo mv hadoop-2.7.0 /usr/local/hadoop" 
os.system(cmd)

import getpass
username = getpass.getuser()
import socket
hostname = socket.gethostname()
cmd = "sudo chown "+username+":sudo -R /usr/local/hadoop/"
os.system(cmd)



cmd = "sudo mkdir -p /usr/local/hadoop_tmp/hdfs/namenode"
os.system(cmd)
cmd = "sudo mkdir -p /usr/local/hadoop_tmp/hdfs/datanode"
os.system(cmd)
cmd = "sudo chown "+username+":sudo -R /usr/local/hadoop_tmp/"
os.system(cmd)

cmd = "cd ~"
os.system(cmd)


cmds = ["echo '# -- HADOOP ENVIRONMENT VARIABLES START -- #' >> ~/.bashrc",
"echo 'export HADOOP_HOME=/usr/local/hadoop' >> ~/.bashrc",
"echo 'export PATH=$PATH:$HADOOP_HOME/bin' >> ~/.bashrc",
"echo 'export PATH=$PATH:$HADOOP_HOME/sbin' >> ~/.bashrc",
"echo 'export HADOOP_MAPRED_HOME=$HADOOP_HOME' >> ~/.bashrc",
"echo 'export HADOOP_COMMON_HOME=$HADOOP_HOME' >> ~/.bashrc",
"echo 'export HADOOP_HDFS_HOME=$HADOOP_HOME' >> ~/.bashrc",
"echo 'export YARN_HOME=$HADOOP_HOME' >> ~/.bashrc",
"echo 'export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native' >> ~/.bashrc",
"echo 'export HADOOP_OPTS=\"-Djava.library.path=$HADOOP_HOME/lib\"' >> ~/.bashrc",
"echo '# -- HADOOP ENVIRONMENT VARIABLES END -- #' >> ~/.bashrc",
"echo '\n' >> ~/.bashrc"]


for i in range(len(cmds)):
    os.system(cmds[i])    


temp  = ''

print("changing xml files")
with open('/usr/local/hadoop/etc/hadoop/hadoop-env.sh', 'r') as content_file:
    content = content_file.read()
    c = str(content)
    temp = c + '\nexport JAVA_HOME=/usr/lib/jvm/java-8-oracle'
   
 
with open('/usr/local/hadoop/etc/hadoop/hadoop-env.sh', 'w+') as content_file:
    content_file.write(temp)


#core-site.xml
with open('/usr/local/hadoop/etc/hadoop/core-site.xml', 'r') as content_file:
    content = content_file.read()
    c = str(content)
    temp = c.replace('<configuration>','')
    temp = temp.replace('</configuration>','')
 
with open('/usr/local/hadoop/etc/hadoop/core-site.xml', 'w+') as content_file:
    temp = temp +'\n<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://localhost:9000</value>\n</property>\n</configuration>'
    content_file.write(temp)

#hdfs-site.xml
with open('/usr/local/hadoop/etc/hadoop/hdfs-site.xml', 'r') as content_file:
    content = content_file.read()
    c = str(content)
    temp = c.replace('<configuration>','')
    temp = temp.replace('</configuration>','')
 
with open('/usr/local/hadoop/etc/hadoop/hdfs-site.xml', 'w+') as content_file:
    temp = temp +'\n<configuration>\n<property>\n<name>dfs.replication</name>\n<value>1</value>\n</property>\n<property>\n<name>dfs.namenode.name.dir</name>\n<value>file:/usr/local/hadoop_tmp/hdfs/namenode</value>\n</property>\n<property>\n<name>dfs.datanode.data.dir</name>\n<value>file:/usr/local/hadoop_tmp/hdfs/datanode</value>\n</property>\n</configuration>'
    content_file.write(temp)

#yarn site-xml
with open('/usr/local/hadoop/etc/hadoop/yarn-site.xml', 'r') as content_file:
    content = content_file.read()
    c = str(content)
    temp = c.replace('<configuration>','')
    temp = temp.replace('</configuration>','')
 
with open('/usr/local/hadoop/etc/hadoop/yarn-site.xml', 'w+') as content_file:
    temp = temp + '\n<configuration>\n<property>\n<name>yarn.nodemanager.aux-services</name>\n<value>mapreduce_shuffle</value>\n</property>\n<property>\n<name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>\n<value>org.apache.hadoop.mapred.ShuffleHandler</value>\n</property>\n</configuration>'
    content_file.write(temp)
    
cmd = "cp /usr/local/hadoop/etc/hadoop/mapred-site.xml.template  /usr/local/hadoop/etc/hadoop/mapred-site.xml"
os.system(cmd)

#mapred-site.xml
with open('/usr/local/hadoop/etc/hadoop/mapred-site.xml', 'r') as content_file:
    content = content_file.read()
    c = str(content)
    temp = c.replace('<configuration>','')
    temp = temp.replace('</configuration>','')

with open('/usr/local/hadoop/etc/hadoop/mapred-site.xml', 'w+') as content_file:
    temp = temp + '\n<configuration>\n<property>\n<name>mapreduce.framework.name</name>\n<value>yarn</value>\n</property>\n</configuration>'
    content_file.write(temp)

cmds = ["sudo chmod 777 /usr/local/hadoop_tmp/hdfs/namenode/",
"hdfs namenode -format",
"start-dfs.sh",
"start-yarn.sh",
"jps"]
for i in range(len(cmds)):
    os.system(cmds[i])










