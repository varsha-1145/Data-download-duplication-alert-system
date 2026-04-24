chrome.downloads.onCreated.addListener(async (downloadItem) => {
  const filename = downloadItem.filename || extractFilename(downloadItem.url);
  const url = downloadItem.url;

  console.log('Download triggered:', { filename, url });

  try {
    const resp = await fetch('http://127.0.0.1:5000/check_duplicate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ filename, url })
    });

    if (!resp.ok) {
      throw new Error(`Server responded with status ${resp.status}`);
    }

    const result = await resp.json();
    console.log('Duplicate check result:', result);

    if (result.is_duplicate === true) {
      chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icon.png',
        title: 'Duplicate Download Detected',
        message: `File already downloaded by ${result.uploader} on ${result.timestamp}.`,
        priority: 2
      });

      chrome.downloads.cancel(downloadItem.id, () => {
        console.log('Duplicate download cancelled.');
      });
    } else {
      console.log('Not a duplicate. Download allowed.');
    }

  } catch (err) {
    console.error('Failed to check duplicate:', err);
  }
});

function extractFilename(url) {
  try {
    const pathname = new URL(url).pathname;
    return pathname.substring(pathname.lastIndexOf('/') + 1) || 'unknown_file';
  } catch (e) {
    console.warn('Could not extract filename from URL:', url);
    return 'unknown_file';
  }
}
