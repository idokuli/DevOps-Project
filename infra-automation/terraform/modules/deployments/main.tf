provider "aws" {
  region = var.aws_region
}

module "custom_vpc_ec2" {
  for_each         = var.instances
  source           = "../custom_vpc_ec2"
  instance_name    = each.key
  vpc_cidr         = "10.0.0.0/16"
  subnet_count     = 3
  ami_id           = each.value.ami_id
  instance_type    = each.value.instance_type
  assign_public_ip = true
}

module "lb_tg_as" {
  for_each               = var.instances
  source                 = "../lb_tg_as"
  instance_name          = each.key
  aws_region             = var.aws_region
  vpc_id                 = module.custom_vpc_ec2[each.key].vpc_id
  public_subnet_ids      = module.custom_vpc_ec2[each.key].public_subnet_id
  security_group_id      = module.custom_vpc_ec2[each.key].sg_id
  source_instance_id     = module.custom_vpc_ec2[each.key].instance_id
  instance_type          = each.value.instance_type
  lb_name                = "lb-${each.key}"
  lb_type                = "application"
  lb_internal            = false
  tg_name                = "tg-${each.key}"
  tg_port                = 80
  tg_protocol            = "HTTP"
  tg_type                = "instance"
  min_size               = 1
  max_size               = 3
  desired_capacity       = 1
  tg_arn                 = "tg_arn"
  tg_id                  = "tg_id"
  lb_port                = 80
  lb_protocol            = "HTTP"
  lb_arn                 = "lb_arn"
  tg_action_type         = "forward"
  tg_action_forward      = "tg_arn"
  policy_name            = "policy-${each.key}"
  policy_type            = "TargetTrackingScaling"
  target_value           = 50
  predefined_metric_type = "ASGAverageCPUUtilization"
  min_healthy_percentage = 75
  max_healthy_percentage = 125
  key_name               = module.custom_vpc_ec2[each.key].key_name
}
