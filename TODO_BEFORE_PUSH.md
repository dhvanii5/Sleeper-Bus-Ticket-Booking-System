# ⚠️ TODO BEFORE GITHUB PUSH

## 🔴 CRITICAL - Must Update

### 1. Author Information (README.md lines 202-204)
Replace these placeholders:
```markdown
**Your Name**  
GitHub: [@yourusername](https://github.com/yourusername)  
Email: your.email@example.com
```

**Update to**:
```markdown
**Dhvani**  
GitHub: [@dhvani123](https://github.com/dhvani123)  # Use your actual GitHub username
Email: dhvani@example.com  # Use your actual email
```

---

### 2. Repository URL (README.md line 49)
Replace:
```bash
git clone https://github.com/yourusername/Sleeper-Bus-Ticket-Booking-System.git
```

**Update to**:
```bash
git clone https://github.com/YOUR_ACTUAL_USERNAME/Sleeper-Bus-Ticket-Booking-System.git
```

---

### 3. Figma Link (README.md line 312)
**Current**:
```markdown
**Figma Link**: [Bus Booking System Wireframes](https://www.figma.com/design/your-design-link)
```

**Options**:
- **If you have Figma design**: Replace with actual public link
- **If no Figma**: Remove this section entirely OR add note "(Design in progress)"

---

## 🟡 OPTIONAL - Nice to Have

### 4. Database Configuration
**File**: `app/config.py`

Check if you want to change default PostgreSQL credentials:
```python
DATABASE_URL = "postgresql+psycopg://postgres:password@localhost:5432/sleeper_bus_db"
```

Consider using environment variable:
```python
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:password@localhost:5432/sleeper_bus_db")
```

---

### 5. Add .env.example (Optional)
Create a template for environment variables:

**File**: `.env.example`
```env
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/sleeper_bus_db
DEBUG_MODE=True
```

---

## ✅ VERIFICATION STEPS

### Step 1: Test Fresh Setup
```bash
# In a new terminal/folder
git clone <your-repo-url>
cd Sleeper-Bus-Ticket-Booking-System
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/init_db.py
uvicorn app.main:app --reload
```

### Step 2: Check Documentation Renders
- Push to GitHub
- Visit repository page
- Verify README.md renders correctly
- Check all links work
- Ensure images/diagrams display (if any)

### Step 3: Run All Tests
```bash
pytest tests/ -v
python tests/test_basic.py
python tests/test_comprehensive.py
```

### Step 4: Verify API Documentation
```bash
# Start server
uvicorn app.main:app --reload

# Open browser
http://localhost:8000/docs
```

Check:
- [ ] All endpoints visible
- [ ] Schemas displayed
- [ ] Try endpoints work
- [ ] Examples shown

---

## 📋 FINAL CHECKLIST

### Documentation
- [ ] Author name updated in README
- [ ] GitHub username updated in README
- [ ] Email updated in README
- [ ] Repository clone URL updated
- [ ] Figma link updated or removed
- [ ] All placeholders replaced

### Code
- [ ] No hardcoded credentials in code
- [ ] `.env` file in `.gitignore`
- [ ] No absolute file paths in code
- [ ] All imports working
- [ ] No TODO/FIXME comments left

### Testing
- [ ] All tests pass
- [ ] Server starts without errors
- [ ] Database initializes correctly
- [ ] ML model trains successfully
- [ ] API docs load at /docs

### Git
- [ ] `.gitignore` includes `.env`, `__pycache__`, `.venv`
- [ ] No sensitive data in git history
- [ ] Commit messages are meaningful
- [ ] Branch is up to date

---

## 🚀 PUSH COMMANDS

```bash
# Check status
git status

# Add all files
git add .

# Commit with meaningful message
git commit -m "Complete sleeper bus booking system with ML predictions

Features:
- Segment-based seat booking with overlap detection
- Dynamic pricing engine
- ML-powered booking confirmation predictions
- Complete booking lifecycle with refunds
- Comprehensive API documentation
- 27+ test cases documented"

# Push to GitHub
git push origin main

# Or if first push
git push -u origin main
```

---

## 📝 COMMIT MESSAGE TEMPLATE

```
Complete sleeper bus booking system with ML predictions

Features:
- Segment-based seat availability (prevents double-booking)
- Dynamic pricing (distance × seat type)
- Logistic Regression prediction model (82% accuracy)
- Comprehensive API with 12 endpoints
- Full documentation (README + PREDICTION_APPROACH)
- 27+ test cases across functional/edge/UX scenarios

Tech Stack:
- FastAPI + PostgreSQL + SQLAlchemy
- Scikit-learn for ML
- Pydantic validation
- Clean architecture (API/Service/Model layers)

Testing:
- pytest test suite
- All endpoints verified
- Edge cases covered
```

---

## ⚠️ COMMON MISTAKES TO AVOID

1. ❌ **Don't commit `.env` file** - Use `.env.example` instead
2. ❌ **Don't hardcode database passwords** - Use environment variables
3. ❌ **Don't leave placeholders** - Update all "Your Name", "yourusername"
4. ❌ **Don't push without testing** - Run tests before commit
5. ❌ **Don't use absolute paths** - Use relative paths only
6. ❌ **Don't commit `__pycache__`** - Ensure in `.gitignore`
7. ❌ **Don't forget requirements.txt** - Include all dependencies

---

## 🎯 QUICK PRE-PUSH TEST

Run this to verify everything works:

```bash
# 1. Clean build
rm -rf .venv __pycache__
python -m venv .venv
.venv\Scripts\activate

# 2. Fresh install
pip install -r requirements.txt

# 3. Initialize
python scripts/init_db.py

# 4. Test
python -m pytest tests/ -v

# 5. Start server
uvicorn app.main:app --reload

# If all pass ✅ = READY TO PUSH
```

---

## 📞 NEED HELP?

If any step fails:
1. Check error message carefully
2. Verify Python version (3.10+)
3. Ensure PostgreSQL is running
4. Check database credentials in config.py
5. Review `.gitignore` includes common files

---

**Status**: ⏳ READY FOR UPDATES  
**After Updates**: ✅ READY TO PUSH

---

**Remember**: Think like a reviewer - "Can I clone and run this in 5 minutes?"
