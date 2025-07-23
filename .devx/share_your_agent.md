# Share Your Agent
<!-- 
<img src="_static/robots/typewriter.png" alt="Share Robot" style="float:right; max-width:300px;margin:25px;" /> -->

Ready to share your AI agent with the world? Let's turn your agent into a Brev launchable so others can use it!

## Step 1: Create Your GitHub Repository

<img src="_static/robots/assembly.png" alt="Build Repository Robot" style="float:right; max-width:250px;margin:25px;" />

**New to GitHub?** [Sign up for free](https://github.com/join)

1. **Create a new repository** at [github.com/new](https://github.com/new)
2. **Name it** something creative that represents your agent
3. **Make it public** so others can see your work
4. **Initialize with README** ✅

<!-- fold:break -->

## Step 2: Push Your Agent

**In your terminal:**

```bash
# Clone your new repo
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

# Copy your notebook and any other files
cp /path/to/your/agent_notebook.ipynb .
cp /path/to/requirements.txt .

# Add and commit
git add .
git commit -m "Add my AI report generation agent"
git push origin main
```

**Don't forget to include:**
- Your completed notebook
- `requirements.txt` with dependencies
- README explaining what your agent does

<!-- fold:break -->

## Step 3: Deploy with Brev

<img src="_static/robots/hero.png" alt="Deploy Robot" style="float:right; max-width:250px;margin:25px;" />

**Make your agent accessible to anyone, anywhere:**

1. **Visit** [console.brev.dev](https://console.brev.dev) and sign up
2. **Click "Create Launchable"**
3. **Input your GitHub repository link** (the one you just created)
4. **Choose your environment container:**
   - Select a Python container [INSERT DEFAULT CONTAINER]
5. **Start building!** 🚀

Brev will automatically build your launchable and give you a public URL that anyone can access.

🎉 **Congratulations!** You've built and deployed your own AI agent!

