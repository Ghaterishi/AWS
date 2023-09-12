# Deploying Node-app On AWS ECS Farget.

## Overview:
We can easily deploy application on ECS farget and access that using ECS task PublicIp, but thats not good practice here you compromise your securtiy as there is no additional layer of security. End user can directly hitting/sending their request to ecs tasks.
Secondly you think lets deploy ECS Task in private subnet, thats a good idea and many apps use the same infrastructure, But DOnt you think their is still some security compriese or loopholes. let me explain, if you want to host your ECS Task in private subnet you need NAT Gateway to pull the images from ECR or anyother work which required internet otherwise you cant access the app..right? Here also internet is accessible from inside the Private subnet and where there is a internet access its not fully secure.

## Best-Practices:
To secure app, we have to build it in most reliable and secure way. We can do one thing Deployed the app on ECS Task which is hosted in Private subnet but its not using NAT Gateway. Now you are wondering then how ECS task will pull images..? 

AWS have something called VPC endpoint or privatelink, which is design for securely access AWS services within your account and main thing is your request is not going via internet. 

## VPC endpoint:
There are two types of endpoint,
- Gateway endpoint
- Interface endpoint

  #### Gateway Endpoint:
  These endpoints allow your VPC to access AWS services using a direct route within the AWS network. currently only two services can support this type which is S3 and DynamoDB.

  #### Interface Endpoint:
  These endpoints are used to connect your VPC to AWS services that are outside of your VPC by creating an Elastic Network Interface (ENI) in your VPC. Most of aws services supports this endpoint.

 ## lets create the infrastructure and deploy the app.
  ### Step-01: Build Docker image
   First fork the below repo and build a docker image.
   
  GitHub repo-[https://github.com/Ghaterishi/node-todo-cicd]
<img width="785" alt="image" src="https://github.com/Ghaterishi/AWS/assets/92510442/d9590388-3dc8-4001-a24a-bf460206b2f3">

  ### Step-02: Create one Private ECR registry and push image in it.
  Login to your AWS account and Search ECR, then you you will land on ECR homepage, then click on repositories option on left sidre panel and create one private registry. 
  <img width="935" alt="image" src="https://github.com/Ghaterishi/AWS/assets/92510442/0ba33f1b-bc63-44c3-827e-e742405c5eb7">

After this click on checkbox mention left side of repo name and click on view push command, follow the instruction and push docker which we build in step-01 into the ECR.
<img width="556" alt="image" src="https://github.com/Ghaterishi/AWS/assets/92510442/fa5246b3-0e04-4f28-a4e7-8c721ac3bfa1">

### Step-03: Setup the VPC
 Create two AZs, 2 public subnet, 2 private subnet and in NAT gatewat select none, we dont need NAT gateway.
 
 <img width="926" alt="image" src="https://github.com/Ghaterishi/AWS/assets/92510442/d58a7a58-8044-4ebd-b0ba-08d034b99a3c">

### Step-04: Associate required VPC Endpoint to the Private subnet
The main issue we are facing without NAT Gateway is our ECS Task will not able to pull images from ECR so we have to attach ECR endpoint and for storging logs logs endpoint.

Now click on endpoints option avaliable on left side panel of vpc homepage, you can see s3 gateway endpoint is already created and associated with your newly created vpc.  click on create endpoint, give name to your endpoint and under service category choose AWS services.

<img width="883" alt="image" src="https://github.com/Ghaterishi/AWS/assets/92510442/89b30593-318f-4bb7-a570-d3642490f428">

In services search for ecr and choose **com.amazonaws.us-east-1.ecr.api** , after this select VPC then tick on each subnet azs checkbox and select private subnet .

<img width="857" alt="image" src="https://github.com/Ghaterishi/AWS/assets/92510442/e21d528f-d66b-4b87-af9e-9df2bec83b4a">

In security group section select security which are used by your ECS tasks in my case i am usig default one. after all the configuration click on create endpoint.

Following same procedure as mentioned above cretate two more endpoint 
- **com.amazonaws.us-east-1.ecr.dkr**
- **com.amazonaws.us-east-1.ecr.logs**

### Step-05: Create a cluster and Task defination
Go to the ECS homepage and create  cluster, while creating cluster choose launch type as Farget. After creating cluster create a task defination, while creating cluste filled the mandtory details like family name,CPU, memory, launch type, container port and in image URI specify the uri image that we push in ECR.

<img width="765" alt="image" src="https://github.com/Ghaterishi/AWS/assets/92510442/487a79d0-072f-42c5-b836-1071f2818837">

### Step-06: Create a Load Balancer and Target Group:
First create a target group choose target type as ip address and configure the remaining deatails, then create application load balancer with lister http 80 and forward that traffic to created target group.
while creating load balancer choose VPC and public subnet which we are already created,

<img width="624" alt="image" src="https://github.com/Ghaterishi/AWS/assets/92510442/d7a923c2-2954-4e5e-8506-505598abd97d">

<img width="627" alt="image" src="https://github.com/Ghaterishi/AWS/assets/92510442/7fb98e26-966e-4a1b-8f65-6620caee5e01">

### Step-07: Create a ECS service and attach load balancer to it.
Open the ECS homepage and click cluster created in Step-05 , scroll up and click on create service, fill the details

<img width="745" alt="image" src="https://github.com/Ghaterishi/AWS/assets/92510442/3497dcee-95f1-4412-89e9-c0280b4fc2a8">

In family choose previously created task defination, fill service name

<img width="495" alt="image" src="https://github.com/Ghaterishi/AWS/assets/92510442/2db99e63-c8af-4094-bcdb-c046af355d2e">

mention desired task as 2, open networking select vpc and private subnet

<img width="509" alt="image" src="https://github.com/Ghaterishi/AWS/assets/92510442/60232582-d3b4-48e3-bbf6-a9bffb6ffbcb">

Open load balancing section and attach previously created load balancer and target group

<img width="485" alt="image" src="https://github.com/Ghaterishi/AWS/assets/92510442/fd816ae1-1721-4017-a645-1ed52eb0d409">

### Step-08: Access the app
It will take around 10 min to create service and then click on service name, go to the networking section and copy the load balancer DNS and paste it in the browser and boom..!

<img width="944" alt="image" src="https://github.com/Ghaterishi/AWS/assets/92510442/d5dfb5e2-1d61-4806-94ba-2755f8e18817">

## Conclusion:
This is the tough one. i encourged you to try this own your own then you will end up this lots more errors try to troubleshoot them. As you troubleshoot errors you will learn alot.

**Thanks for reading happy learning**

