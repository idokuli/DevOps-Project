variable "instance_name" {
  type = string
}

variable "vpc_cidr" {
  type = string
}
variable "subnet_count" {
  type = number
}
variable "instance_type" {
  type    = string
  default = "t3.micro"
}
variable "ami_id" {
  type    = string
  default = null
}
variable "assign_public_ip" {
  type = bool
}
