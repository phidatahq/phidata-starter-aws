from workspace.settings import ws_name

# -*- Dev settings

dev_env = "dev"
# Key for dev resources
dev_key = f"{ws_name}-{dev_env}"
# Tags for dev resources
dev_tags = {
    "env": dev_env,
    "project": ws_name,
}
