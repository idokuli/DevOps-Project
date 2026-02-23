data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}
resource "aws_vpc" "main_vpc" {
  cidr_block = var.vpc_cidr
  tags = {
    Name = "main_vpc"
  }
}
resource "aws_subnet" "public_subnet" {
  count             = var.subnet_count
  vpc_id            = aws_vpc.main_vpc.id
  cidr_block        = "10.0.${count.index}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index % length(data.aws_availability_zones.available.names)]
  tags = {
    Name = "public_subnet-${count.index}"
  }
}
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main_vpc.id
  tags = {
    Name = "igw"
  }
}
resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.main_vpc.id
  tags = {
    Name = "public_route_table"
  }
}
resource "aws_route" "public_route" {
  route_table_id         = aws_route_table.public_route_table.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}
resource "aws_route_table_association" "public_route_table_association" {
  count          = var.subnet_count
  subnet_id      = aws_subnet.public_subnet[count.index].id
  route_table_id = aws_route_table.public_route_table.id
}
resource "aws_security_group" "sg" {
  name        = "sg"
  description = "Security Group"
  vpc_id      = aws_vpc.main_vpc.id
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "sg"
  }
}
resource "tls_private_key" "generated" {
  algorithm = "RSA"
  rsa_bits  = 4096
}
resource "local_file" "private_key" {
  content         = tls_private_key.generated.private_key_pem
  filename        = "id_rsa_${var.instance_name}.pem"
  file_permission = "0400"
}
resource "aws_key_pair" "deployer" {
  key_name   = "deployer-key-${var.instance_name}"
  public_key = tls_private_key.generated.public_key_openssh
}
resource "aws_instance" "instance1" {
  ami                         = var.ami_id != null ? var.ami_id : data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.public_subnet[var.subnet_count - 1].id
  associate_public_ip_address = var.assign_public_ip
  vpc_security_group_ids      = [aws_security_group.sg.id]
  key_name                    = aws_key_pair.deployer.key_name
  monitoring                  = true
  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = tls_private_key.generated.private_key_pem
    host        = self.public_ip
  }
  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y software-properties-common",
      "sudo add-apt-repository -y universe",
      "sudo apt-get update",
      "sudo apt-get install -y nginx stress-ng",
      "echo '<h1>Healthy</h1>' | sudo tee /var/www/html/index.html"
    ]
  }
  tags = {
    Name = var.instance_name
  }
}
