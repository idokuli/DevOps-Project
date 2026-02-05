variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "instances" {
  description = "A map of instances to create"
  type = map(object({
    name          = string
    region        = string
    ami_id        = string
    instance_type = string
  }))
  default = {}
}
