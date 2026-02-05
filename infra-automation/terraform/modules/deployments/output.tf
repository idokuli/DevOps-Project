output "vpc_ids" {
  value = { for k, v in module.custom_vpc_ec2 : k => v.vpc_id }
}

output "instance_ids" {
  value = { for k, v in module.custom_vpc_ec2 : k => v.instance_id }
}

output "instance_public_ips" {
  value = { for k, v in module.custom_vpc_ec2 : k => v.instance_public_ip }
}

output "lb_dns_names" {
  value = { for k, v in module.lb_tg_as : k => v.lb_dns_name }
}
