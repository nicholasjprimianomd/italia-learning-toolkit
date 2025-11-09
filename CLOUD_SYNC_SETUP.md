# Cross-Device Progress Sync Setup

Your app now supports syncing progress across devices! Here's how to set it up:

## Quick Start (No Setup Required)

The app works **without any setup** - it will save progress locally in your browser. To enable cross-device sync, follow these steps:

## Option 1: Using JSONBin.io (Free, Recommended)

1. **Create a free account** at https://jsonbin.io
2. **Get your API key**:
   - After logging in, go to "API Keys" section
   - Copy your "X-Master-Key" (this is your API key)
3. **Create a new bin** using one of these methods:

   **Method A: Using the API (Recommended)**
   - Use this command in PowerShell (replace `YOUR_API_KEY` with your actual key):
   ```powershell
   curl.exe -H "Content-Type: application/json" -H "X-Master-Key: YOUR_API_KEY" --request POST --data '{\"users\": {}}' https://api.jsonbin.io/v3/b
   ```
   - The response will include a `id` field - that's your Bin ID!
   - Copy that Bin ID

   **Method B: Using the Web Interface**
   - Go to https://jsonbin.io/app
   - Click "Create Bin" or "New Bin"
   - In the JSON editor, put: `{"users": {}}` (this initializes the structure for user data)
   - Click Save/Create
   - Copy the Bin ID from the URL or bin details

4. **Set environment variables** in Render:
   - Go to your Render service → Environment
   - Add these variables:
     - `JSONBIN_API_KEY` = Your X-Master-Key from step 2
     - `JSONBIN_BIN_ID` = Your Bin ID from step 3

## Option 2: Use Your Own Backend

If you prefer to use your own backend API:

1. Create an API endpoint that accepts GET/PUT requests
2. Set `PROGRESS_API_URL` environment variable to your API endpoint
3. Update `progress_api.py` to match your API format

## How to Use

1. **Open the app** and click the **Settings icon** (⚙️) in the top right
2. **Enter a User ID** - this can be anything unique (email, username, etc.)
3. **Click "Save ID"**
4. **Your progress will now sync** across all devices using the same User ID!

## Notes

- Progress saves automatically after each answer
- If cloud sync fails, it falls back to local storage
- Each exercise type (Articles, Verbs, Prepositions) syncs separately
- Your User ID is stored locally in your browser

## Troubleshooting

- **Progress not syncing?** Check that your JSONBin API key and Bin ID are set correctly in Render
- **Want to use local storage only?** Leave User ID empty
- **Want to reset progress?** Use the "Reset progress" button in each exercise

