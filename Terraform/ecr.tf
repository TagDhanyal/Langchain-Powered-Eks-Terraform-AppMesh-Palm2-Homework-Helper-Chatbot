resource "aws_ecr_repository" "homework-helper" {
  name                 = "homework-helper"
  image_tag_mutability = "MUTABLE"
  force_delete = true 
  

  image_scanning_configuration {
    scan_on_push = true
  }
}