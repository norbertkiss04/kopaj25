const SmeeClient = require('smee-client')
const { exec } = require('child_process')

// Function to execute git pull
function executeGitPull() {
  console.log('Received webhook - executing git pull...')
  
  exec('git pull', (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing git pull: ${error.message}`)
      return
    }
    if (stderr) {
      console.error(`Git pull stderr: ${stderr}`)
      return
    }
    console.log(`Git pull successful: ${stdout}`)
  })
}

// Create a simple HTTP server to receive webhook events
const http = require('http')

const server = http.createServer((req, res) => {
  // Log the incoming request
  console.log(`${new Date().toISOString()} - ${req.method} ${req.url}`)
  
  // Execute git pull for any incoming request
  executeGitPull()
  
  // Send response
  res.writeHead(200, { 'Content-Type': 'text/plain' })
  res.end('Webhook received - git pull executed\n')
})

// Start the server on a random available port
server.listen(0, () => {
  const port = server.address().port
  console.log(`Webhook server listening on port ${port}`)
  
  // Configure smee to forward to our local server
  const smee = new SmeeClient({
    source: 'https://smee.io/MJrgOjEFCSnbJULO',
    target: `http://localhost:${port}`,
    logger: console
  })

  const events = smee.start()
  
  // Handle graceful shutdown
  process.on('SIGINT', () => {
    console.log('\nShutting down...')
    events.close()
    server.close(() => {
      console.log('Server closed')
      process.exit(0)
    })
  })
})