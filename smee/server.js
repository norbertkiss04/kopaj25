(async () => {
  // ESM csomag dinamikus importtal (CJS projektben ez kell)
  const SmeeClient = (await import('smee-client')).default;
  const { exec } = require('child_process');
  const http = require('http');

  // Function to execute git pull
  function executeGitPull() {
    console.log('Received webhook - executing git pull...');

    exec('git pull origin master', (error, stdout, stderr) => {
      if (error) {
        console.error(`Error executing git pull: ${error.message}`);
        return;
      }
      if (stderr) {
        console.error(`Git pull stderr: ${stderr}`);
        return;
      }
      console.log(`Git pull successful: ${stdout}`);
    });
  }

  // Create a simple HTTP server to receive webhook events
  const server = http.createServer((req, res) => {
    console.log(`${new Date().toISOString()} - ${req.method} ${req.url}`);

    // Execute git pull for each request
    executeGitPull();

    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('Webhook received - git pull executed\n');
  });

  // Start server on any free port
  server.listen(0, () => {
    const port = server.address().port;
    console.log(`Webhook server listening on port ${port}`);

    // Start Smee forwarder
    const smee = new SmeeClient({
      source: 'https://smee.io/MJrgOjEFCSnbJULO',
      target: `http://localhost:${port}`,
      logger: console
    });

    const events = smee.start();

    // Graceful shutdown
    process.on('SIGINT', () => {
      console.log('\nShutting down...');
      events.close();
      server.close(() => {
        console.log('Server closed');
        process.exit(0);
      });
    });
  });
})();
