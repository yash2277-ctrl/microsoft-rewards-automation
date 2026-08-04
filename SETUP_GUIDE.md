# Setup Guide for Microsoft Rewards Automation

## Prerequisites

1. **Microsoft Edge Browser** - Must be installed on your system
2. **Python 3.8 or higher** - Download from python.org
3. **4 Microsoft Accounts** - With Rewards enabled

## Step-by-Step Setup

### 1. Install Python Dependencies

Open Command Prompt or PowerShell and navigate to the project folder:

```bash
pip install -r requirements.txt
```

### 2. Setup Edge Profiles

You need to create separate profiles in Microsoft Edge for each account:

1. Open Microsoft Edge
2. Click on your profile icon (top right)
3. Click "Add profile"
4. Sign in with your first Microsoft account
5. Name it "Profile 1"
6. Repeat for your other 3 accounts (Profile 2, Profile 3, Profile 4)

**Important:** Make sure you're signed into Microsoft Rewards on each profile by visiting https://rewards.microsoft.com

### 3. Configure config.json

Edit the `config.json` file with your profile names:

```json
{
  "profiles": [
    {
      "name": "Account 1",
      "edge_profile_name": "Profile 1",
      "pc_searches": 30,
      "mobile_searches": 20
    }
    // ... add your other profiles
  ]
}
```

**Important Settings:**

- `edge_profile_name`: Must match EXACTLY the profile name in Edge
- `pc_searches`: Number of PC searches (usually 30 for 150 points)
- `mobile_searches`: Number of mobile searches (usually 20 for 100 points)
- `headless`: Set to `false` to see the browser, `true` to run hidden

### 4. Test Run

Start with one profile first to test:

1. In `config.json`, keep only one profile temporarily
2. Run: `python main.py`
3. Press Enter when prompted
4. Watch the automation work

### 5. Run Full Automation

Once tested, add all 4 profiles to `config.json` and run:

```bash
python main.py
```

## Finding Your Edge Profile Names

If you're not sure about your profile names:

1. Open Edge
2. Type in address bar: `edge://version`
3. Look for "Profile path"
4. The last part of the path is your profile name
5. Common names: "Default", "Profile 1", "Profile 2", etc.

## Troubleshooting

### "Profile not found" error
- Check that profile names in config.json match EXACTLY with Edge profile names
- Profile names are case-sensitive

### "WebDriver not found" error
- The script will auto-download the driver on first run
- Make sure you have internet connection

### Searches not completing
- Make sure you're logged into Microsoft account in each Edge profile
- Visit https://rewards.microsoft.com manually first in each profile

### "Points not adding" issue
- Microsoft has daily limits (usually 150 PC + 100 mobile points)
- If limits are reached, points won't increase
- Try again the next day

## Daily Usage

Simply run this command each day:

```bash
python main.py
```

The script will:
1. Open Edge with Profile 1
2. Perform all PC searches
3. Perform all mobile searches
4. Switch to Profile 2
5. Repeat for all 4 profiles
6. Stop automatically when done

## Safety Tips

⚠️ **Important:**
- Don't run the script multiple times per day
- Respect Microsoft's daily limits
- Don't modify the search delays (could trigger detection)
- Use responsibly

## Schedule Automation (Optional)

### Windows Task Scheduler:

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Daily at a specific time
4. Action: Start a program
5. Program: `python`
6. Arguments: `C:\path\to\main.py`
7. Start in: `C:\path\to\project\folder`

Now it runs automatically every day!
