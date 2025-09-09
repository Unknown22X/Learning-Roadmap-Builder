<!-- # Learning Roadmap Builder -->
<!-- 
A command-line tool for organizing and tracking your learning goals.

## Usage

- Simple CLI interface
- Example commands provided in documentation

**Requirements:**  
- Python 3 (no external libraries needed) -->

# 🎯 Learning Roadmap Builder

> Your Personal Learning Companion - Transform your learning journey with beautiful, interactive roadmaps!

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-Active-brightgreen.svg)]()

## ✨ Overview

Learning Roadmap Builder is a beautiful, terminal-based application that helps you organize, track, and visualize your learning journey. Whether you're mastering programming languages, developing new skills, or pursuing educational goals, this tool transforms your progress into an engaging, visual experience.

## 🌟 Key Features

### 📋 **Roadmap Management**
- Create unlimited learning roadmaps
- Organize roadmaps by categories (Programming, Design, Languages, Business, etc.)
- Add custom categories for personalized organization
- Edit roadmap titles and descriptions

### ✅ **Progress Tracking**
- Break down learning goals into manageable steps
- Mark steps as complete/incomplete
- Visual progress bars with completion percentages
- Real-time statistics and analytics

### 🎨 **Beautiful Visualizations**
- Rich, colorful terminal interface powered by Rich library
- Animated welcome screens and loading effects
- Progress visualization with emojis and color coding
- Motivational messages based on your progress level

### 🗂️ **Organization Tools**
- Category management system
- Sort roadmaps by title, progress, or category
- Filter roadmaps by category
- Comprehensive overview dashboards

### 💾 **Data Management**
- Import/Export roadmaps as JSON files
- Automatic data persistence
- Backup and share your learning paths
- Safe deletion with confirmation prompts

### 🎯 **Smart Analytics**
- Overall progress tracking across all roadmaps
- Category-wise progress breakdowns
- Completion statistics and trends
- Performance insights and recommendations

## 🚀 Quick Start

### Prerequisites

Make sure you have Python 3.10+ installed on your system.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/learning-roadmap-builder.git
   cd learning-roadmap-builder
   ```

2. **Install required dependencies:**
   ```bash
   pip install rich matplotlib numpy
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

### First Steps

1. **Launch the app** - You'll be greeted with an animated welcome screen
2. **Create your first roadmap** - Choose option 2 from the main menu
3. **Add learning steps** - Use option 3 to break down your goals
4. **Track progress** - Mark steps complete with option 4
5. **Visualize progress** - See beautiful progress displays with option 10

## 📖 Detailed Usage Guide

### Creating Roadmaps

1. Select **"Create Roadmap"** from the main menu
2. Choose an existing category or create a new one
3. Enter a descriptive title for your learning path
4. Start adding steps to build your roadmap

### Managing Categories

Access the **"Manage Categories"** section to:
- View all categories with roadmap counts
- Add new categories for better organization
- Delete unused categories (with safety checks)

### Progress Visualization

The **"Progress Visualization"** feature offers:
- 🎯 Overall learning statistics
- 📊 Individual roadmap progress bars
- ✅ Completed vs. pending steps breakdown
- 💪 Motivational messages based on your achievements

### Import/Export

- **Export**: Share your roadmaps or create backups
- **Import**: Load roadmaps from other users or restore backups
- All data is saved in easy-to-read JSON format

## 🎨 Interface Overview

### Main Menu Sections

| Section | Description | Color Theme |
|---------|-------------|-------------|
| 📊 **View & Track** | Progress viewing and analytics | Blue |
| 🛠️ **Create & Manage** | Content creation and editing | Green |
| 🗂️ **Organize** | Categories and sorting tools | Yellow |
| 🔧 **Tools & Utilities** | Import/export and maintenance | Magenta |

### Progress Indicators

- 💤 **Not Started** (0%) - Ready to begin!
- 🌱 **Beginning** (<25%) - Getting started
- 🚶‍♂️ **Progressing** (<50%) - Making progress  
- 🚀 **Good Pace** (<75%) - Great momentum!
- 🔥 **Almost There** (<100%) - Final push!
- 🎉 **Completed** (100%) - Achievement unlocked!

## 📁 File Structure

```
learning-roadmap-builder/
├── main.py                 # Main application file
├── data.json              # Your roadmap data (auto-generated)
├── README.md              # This file
└── requirements.txt       # Dependencies list
```

## 🛠️ Technical Details

### Dependencies

- **Rich**: Terminal styling and beautiful interfaces
- **Matplotlib**: Future charting capabilities
- **NumPy**: Data processing and analytics
- **JSON**: Data persistence and import/export

### Data Storage

All data is stored in `data.json` with the following structure:

```json
{
  "categories": ["Programming", "Design", "Languages"],
  "roadmaps": [
    {
      "title": "Learn Python",
      "category": "Programming",
      "steps": [
        {
          "title": "Basic Syntax",
          "done": true
        }
      ]
    }
  ]
}
```

## 🎯 Use Cases

### For Students
- Track course progress and assignments
- Organize study materials by subject
- Set and achieve academic milestones

### For Professionals
- Plan skill development paths
- Track certification progress
- Organize training programs

### For Self-Learners
- Structure independent learning
- Track online course completion
- Visualize knowledge acquisition

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Areas for Contribution

- 🌐 Web interface development
- 📱 Mobile companion app
- 📈 Advanced analytics features
- 🎨 Additional themes and customization
- 🔗 Integration with learning platforms

## 🐛 Troubleshooting

### Common Issues

**Q: The interface looks broken or has display issues**
- Ensure your terminal supports Unicode and colors
- Try using a modern terminal like Windows Terminal, iTerm2, or GNOME Terminal

**Q: Data not saving between sessions**
- Check file permissions in the application directory
- Ensure you have write access to the folder

**Q: Import/Export not working**
- Verify JSON file format is valid
- Check file paths and permissions

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Rich Library** - For making terminal applications beautiful
- **Python Community** - For continuous inspiration and support
- **All Contributors** - Thank you for making this project better!

## 📞 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/yourusername/learning-roadmap-builder/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/yourusername/learning-roadmap-builder/discussions)
- 📧 **Email**: your.email@example.com

---

<div align="center">

**Made with ❤️ for learners everywhere**

⭐ Star this repo if it helped you organize your learning journey!

</div>