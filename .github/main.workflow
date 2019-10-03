workflow "Push it" {
  resolves = ["Upgrade to Python 3"]
  on = "push"
}

action "Upgrade to Python 3" {
  secrets = ["GITHUB_TOKEN"]
  uses = "cclauss/Upgrade-to-Python3@master"
}
