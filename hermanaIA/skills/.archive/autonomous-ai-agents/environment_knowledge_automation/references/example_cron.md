# Example Cron Commands for Environment Knowledge Automation

## Basic Examples

### Run every 6 hours (recommended)
```bash
hermes cron create "0 */6 * * *" --script descubrir_entorno.sh --no-agent --name "Entorno descubrimiento"
```

### Run daily at 2 AM
```bash
hermes cron create "0 2 * * *" --script descubrir_entorno.sh --no-agent --name "Descubrimiento diario"
```

### Run every weekday at 9 AM
```bash
hermes cron create "0 9 * * 1-5" --script descubrir_entorno.sh --no-agent --name "Descubrimiento laboral"
```

### Run every 12 hours with delivery to a specific chat
```bash
hermes cron create "0 */12 * * *" --script descubrir_entorno.sh --no-agent --deliver "telegram:-1001234567890:12345" --name "Entorno Telegram"
```

### Run with specific skills preloaded (if needed)
```bash
hermes cron create "0 */6 * * *" --script descubrir_entorno.sh --skills "hermes-agent,hermes-agent-skill-authoring" --no-agent --name "Descubrimiento con skills"
```

## Managing Cron Jobs

### List all cron jobs
```bash
hermes cron list
```

### Run a job manually (to test)
```bash
hermes cron run <JOB_ID>
```

### Pause/Resume a job
```bash
hermes cron pause <JOB_ID>
hermes cron resume <JOB_ID>
```

### Remove a job
```bash
hermes cron remove <JOB_ID>
```

## Tips for Optimal Performance

1. **Keep intervals reasonable**: Every 6 hours is a good balance for most environments
2. **Monitor output size**: The script limits output (head -30) to prevent excessive growth
3. **Consider system load**: Avoid scheduling during peak usage times if your system is resource-constrained
4. **Review logs**: Check `~/.hermes/logs/cron.log` for execution history
5. **Adjust exclusions**: Modify the EXCLUDE_DIRS variable in the script if you need to track different directories