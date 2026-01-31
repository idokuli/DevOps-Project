resource "aws_vpc" "main_vpc" {
  cidr_block = "10.20.10.0/24"
  tags = {
    name = "Project's_VPC"
  }
}
resource "aws_subnet" "subnet1" {
  vpc_id     = aws_vpc.main_vpc.id
  cidr_block = "10.20.10.0/28"
  tags = {
    name = "Project's_subnet1"
  }
}
resource "aws_subnet" "subnet2" {
  vpc_id     = aws_vpc.main_vpc.id
  cidr_block = "10.20.10.16/28"
  tags = {
    name = "Project's_subnet2"
  }
}
resource "aws_route_table" "route_table" {
  vpc_id = aws_vpc.main_vpc.id
  tags = {
    name = "Project's_route_table"
  }
}
resource "aws_route_table_association" "route_table_association" {
  subnet_id      = aws_subnet.subnet1.id
  route_table_id = aws_route_table.route_table.id
}
resource "aws_route_table_association" "route_table_association2" {
  subnet_id      = aws_subnet.subnet2.id
  route_table_id = aws_route_table.route_table.id
}
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main_vpc.id
  tags = {
    name = "Project's_igw"
  }
}
resource "aws_route" "route" {
  route_table_id         = aws_route_table.route_table.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}
