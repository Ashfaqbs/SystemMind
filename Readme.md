# SystemMind 🖥️🧠

![Image](/assets/image.png)

**A Universal Operating System Management MCP Server for Intelligent System Operations**

SystemMind is an MCP (Model Context Protocol) server that provides AI assistants with powerful cross-platform system management capabilities. It enables seamless monitoring, diagnostics, and analysis of operating systems through natural language interactions across Windows, macOS, and Linux.

## 🎯 What is SystemMind?

SystemMind bridges the gap between AI assistants (like Claude) and operating systems, allowing you to monitor, diagnose, and optimize your computer using conversational interfaces. It's a unified API that works across multiple operating systems, providing real-time insights and diagnostic capabilities.

## 🔥 Problem It Solves

### The Challenge
Modern computer users and administrators often face these issues:
- **Platform fragmentation**: Different commands and tools for Windows, macOS, and Linux
- **Complex diagnostics**: Navigating through multiple system utilities to identify issues
- **Performance visibility**: Difficult to get quick insights into system resource usage
- **Manual troubleshooting**: Time-consuming manual checks for system health and bottlenecks
- **Context switching**: Jumping between Task Manager, Activity Monitor, top, and various CLI tools
- **Technical barriers**: Non-technical users struggle with command-line diagnostics

### The Solution
SystemMind provides:
- **Unified interface** across Windows, macOS, and Linux
- **AI-powered diagnostics** through natural language queries
- **Real-time monitoring** with easy-to-parse metrics
- **Automated performance analysis** for troubleshooting system issues
- **Single entry point** for all OS operations
- **User-friendly output** that explains technical concepts simply

## 🚀 Features

### Multi-Platform Support
- ✅ **Windows** - Full support for Windows 10/11
- ✅ **macOS** - Complete macOS compatibility
- ✅ **Linux** - Ubuntu, Debian, RHEL, CentOS, and other distributions
- 🔄 **Auto-detection** - Automatically detects OS and adapts accordingly
- 🔌 **Pluggable architecture** - Consistent API across all platforms

### Comprehensive System Operations

#### 📊 System Information
- Complete hardware specifications (CPU, RAM, storage)
- Operating system details and architecture
- Current resource utilization metrics
- System uptime and boot time

#### 🔍 Process Management
- List all running processes with resource usage
- Identify top memory and CPU consumers
- Process categorization (applications, system, browsers, dev tools)
- Real-time process monitoring

#### ⚡ Performance Monitoring
- CPU usage and core statistics
- Memory usage with swap/page file details
- Disk I/O statistics and space utilization
- Network activity and connection monitoring
- Battery status and power management (for laptops)
- Temperature monitoring (Linux/macOS)

#### 🔧 Diagnostics & Optimization
- Comprehensive performance diagnostics
- Startup program analysis and impact assessment
- Resource bottleneck identification
- Large file discovery for disk cleanup
- Security status checks
- Health scoring with actionable recommendations

## 🛠️ Available Tools

| Tool | Description | Use Case |
|------|-------------|----------|
| `initialize_os_connection` | Detect and initialize OS | Initial setup, platform detection |
| `get_system_overview` | Complete system specifications | Hardware info, capacity planning |
| `get_running_processes` | List active processes | Identify resource-heavy apps |
| `get_performance_summary` | Quick health check | Overall system status assessment |
| `get_network_info` | Network status and usage | Connectivity troubleshooting |
| `get_disk_usage` | Storage capacity and I/O | Disk space management |
| `get_battery_info` | Battery status (laptops) | Power management, battery health |
| `get_temperature_info` | System temperatures | Overheating detection (Linux/macOS) |
| `check_startup_programs` | Startup applications list | Boot time optimization |
| `get_user_info` | Current user and sessions | User management, session info |
| `find_large_files` | Locate space-consuming files | Disk cleanup, storage optimization |
| `get_installed_software` | List installed applications | Software inventory |
| `check_security_status` | Security configuration audit | Antivirus status, security score |
| `get_system_services` | Running system services | Service management |
| `get_resource_monitor` | Real-time resource tracking | Live performance monitoring |
| `diagnose_slow_performance` | Comprehensive diagnostics | Troubleshoot slowness issues |
| `get_power_settings` | Power management info | Battery optimization, performance modes |

## 💡 How SystemMind Helps

### 1. **Performance Troubleshooting**
**Scenario**: Computer running slowly
```
You: "My computer is running slow, what's wrong?"
AI: [Uses diagnose_slow_performance + get_running_processes]
    "Performance Analysis Complete:
     - Chrome is using 3.5 GB RAM across 15 tabs
     - CPU usage is normal at 18%
     - Memory usage is high at 85%
     
     Root Cause: Memory pressure from browser tabs
     
     Recommendations:
     1. Close unused Chrome tabs (will free ~2 GB)
     2. Restart Chrome to clear memory leaks
     3. Consider adding more RAM if this happens frequently"
```

### 2. **Resource Optimization**
**Scenario**: Optimizing system startup
```
You: "My laptop takes forever to start, can you help?"
AI: [Uses check_startup_programs + get_performance_summary]
    "Startup Analysis:
     - 45 programs launch at startup
     - Consuming 2.8 GB RAM before you open anything
     - Estimated boot impact: 45-60 seconds
     
     Top startup memory users:
     1. Dropbox: 450 MB
     2. Spotify: 320 MB
     3. Steam: 280 MB
     
     Recommendation: Disable these 3 programs from startup
     Potential improvement: 30-40 second faster boot time"
```

### 3. **Disk Space Management**
**Scenario**: Running out of storage
```
You: "I'm running out of disk space, what's taking up room?"
AI: [Uses get_disk_usage + find_large_files]
    "Storage Analysis:
     - Total: 1 TB
     - Used: 890 GB (89%) - Almost full!
     - Free: 110 GB
     
     Largest files found:
     1. VirtualBox VM: 85 GB
     2. Old backups: 45 GB
     3. Downloaded videos: 23 GB
     
     Quick wins:
     - Delete old VM snapshots: ~30 GB
     - Remove outdated backups: ~45 GB
     - Potential recovery: 75 GB"
```

### 4. **Security Audit**
**Scenario**: Security health check
```
You: "Is my computer secure?"
AI: [Uses check_security_status + get_system_overview]
    "Security Assessment:
     
     ✅ Windows Defender: Active and running
     ✅ Firewall: Enabled
     ✅ System Updates: Current (last restart 3 days ago)
     ⚠️  Windows uptime: 45 days - updates pending
     
     Security Score: 85/100
     
     Recommendations:
     1. Restart to apply pending security updates
     2. Enable automatic updates
     
     Overall: Your system has good basic security"
```

### 5. **System Health Monitoring**
**Scenario**: Proactive system check
```
You: "Give me a health report of my computer"
AI: [Uses get_performance_summary + get_system_overview + get_battery_info]
    "System Health Report:
     
     Overall Status: 🟢 EXCELLENT (92/100)
     
     Hardware:
     - CPU: 8 cores, 18% usage ✅
     - RAM: 16 GB, 42% usage ✅
     - Storage: 550 GB free (55%) ✅
     - Battery: 85% (charging) ✅
     
     Performance:
     - No bottlenecks detected
     - All resources within normal range
     - System uptime: 2 days
     
     Your computer is running optimally!"
```

### 6. **Temperature Monitoring** (Linux/macOS)
**Scenario**: Overheating concerns
```
You: "My laptop feels hot, check the temperatures"
AI: [Uses get_temperature_info + get_resource_monitor]
    "Temperature Analysis:
     
     CPU Temperatures:
     - Core 0: 78°C ⚠️
     - Core 1: 82°C ⚠️
     - Core 2: 79°C ⚠️
     - Core 3: 81°C ⚠️
     
     Status: Running warm under load
     
     Current Activity:
     - CPU usage spiking to 95% during video encoding
     
     Recommendations:
     1. Ensure proper ventilation
     2. Clean dust from vents
     3. Consider laptop cooling pad
     4. Check if thermal paste needs replacement (if old laptop)"
```

### 7. **Network Diagnostics**
**Scenario**: Connectivity issues
```
You: "My internet seems slow, what's using bandwidth?"
AI: [Uses get_network_info + get_resource_monitor + get_running_processes]
    "Network Analysis:
     
     Connection: Wi-Fi @ 866 Mbps
     
     Current Activity (last 5 seconds):
     - Download: 4.2 MB/s
     - Upload: 850 KB/s
     
     Bandwidth consumers:
     1. Steam: Downloading game update
     2. OneDrive: Syncing files
     3. Chrome: Streaming video
     
     Your connection is fine, but multiple apps are competing
     for bandwidth. Pause Steam download for better browsing."
```

### 8. **Battery Optimization**
**Scenario**: Poor battery life
```
You: "My battery drains too quickly, help me optimize it"
AI: [Uses get_battery_info + get_power_settings + get_running_processes]
    "Battery Optimization Analysis:
     
     Current Status:
     - Battery: 45% (3.2 hours remaining)
     - Power Mode: High Performance ⚠️
     - Screen Brightness: 100% ⚠️
     
     Power-hungry processes:
     - Chrome: 15% CPU (multiple tabs)
     - Spotify: Playing music
     - OneDrive: Syncing
     
     Recommendations:
     1. Switch to 'Balanced' power mode (+45 min)
     2. Reduce brightness to 60% (+30 min)
     3. Close unused Chrome tabs (+20 min)
     4. Pause OneDrive sync while on battery (+15 min)
     
     Potential improvement: 1.5 hours extra battery life"
```

## 📋 Installation & Setup

### Prerequisites
- Python 3.8+
- Operating System: Windows 10/11, macOS 10.14+, or Linux
- Required Python packages: `psutil`, `fastmcp`

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Server
```bash
python OS_mcp_server.py
```

The server starts and is ready for MCP connections.

### Configure with Claude Desktop

Add to your Claude Desktop configuration (`claude_desktop_config.json`):

**claude:**
```json
{"mcpServers": {
"OS-Mcp": {
    "command": "uv",
    "args": [
        "run",
        "--with",
        "fastmcp",
        "fastmcp",
        "run",
        "path\\to\\proxy.py" 
    ],
    "env": {},
    "transport": "stdio"
}

    }
    
}
```

**Continue.dev**
```yaml
name: Sample MCP
version: 0.0.1
schema: v1
mcpServers:
  - name: SystemMind MCP server
    type: streamable-http
    url: http://127.0.0.1:9090/mcp/
```

## 🔧 Usage Examples

For detailed usage examples, please refer to the [example folder](./example/Readme.md).



## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         AI Assistant (Claude)           │
└────────────────┬────────────────────────┘
                 │ MCP Protocol
┌────────────────▼────────────────────────┐
│          SystemMind Server              │
│  ┌─────────────────────────────────┐   │
│  │    Tool Interface Layer         │   │
│  │   (17 diagnostic tools)         │   │
│  └──────────────┬──────────────────┘   │
│  ┌──────────────▼──────────────────┐   │
│  │   OS Detection & Abstraction    │   │
│  └──────────────┬──────────────────┘   │
│  ┌──────────────▼──────────────────┐   │
│  │   Platform-Specific Handlers    │   │
│  │  ┌────────┐ ┌──────┐ ┌───────┐  │   │
│  │  │Windows │ │macOS │ │ Linux │  │   │
│  │  └───┬────┘ └──┬───┘ └───┬───┘  │   │
│  └──────┼─────────┼─────────┼─────┘   │
└─────────┼─────────┼─────────┼─────────┘
          │         │         │
    ┌─────▼─────┐ ┌─▼─────┐ ┌─▼──────┐
    │  Windows  │ │ macOS │ │ Linux  │
    │    OS     │ │  OS   │ │   OS   │
    └───────────┘ └───────┘ └────────┘
```

## 🔐 Security Considerations

- SystemMind requires standard user-level permissions (no root/admin required for most operations)
- Some operations may have limited access on restricted system directories
- No authentication layer (relies on MCP transport security)
- Does not modify system state (read-only diagnostics)
- Exception: `clean_temp_files` is the only tool that modifies files (disabled by default)
- Recommended: Use in trusted environments or add authentication for remote access

## 🎨 Output Formatting

SystemMind uses emoji-rich, user-friendly formatting:
- 🟢 Green indicators for healthy status
- 🟡 Yellow for warnings
- 🔴 Red for critical issues
- ✅ Checkmarks for good status
- ⚠️ Warning symbols for attention items
- 📊 Charts and visual representations where applicable

## 🚧 Roadmap

### Planned Features
- [ ] Advanced network diagnostics (port scanning, connection testing)
- [ ] Automated cleanup suggestions with one-click actions
- [ ] Historical performance tracking
- [ ] Export diagnostics reports (PDF/JSON)
- [ ] Web UI dashboard


### Platform-Specific Enhancements
- [ ] Windows: Registry health checks
- [ ] macOS: Spotlight indexing status
- [ ] Linux: systemd service management

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional platform-specific diagnostics
- Enhanced metrics visualization
- Performance optimizations
- Expanded hardware monitoring
- Documentation improvements
- Test coverage expansion

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📊 Comparison: SystemMind vs ContainMind

| Feature | SystemMind | ContainMind |
|---------|-----------|-------------|
| **Scope** | Operating Systems | Containers |
| **Target** | System administrators, end users | DevOps, developers |
| **Platforms** | Windows, macOS, Linux | Docker, Podman |
| **Use Case** | System health, performance | Container orchestration |
| **Complexity** | User-friendly, accessible | Technical, developer-focused |
| **Integration** | Works together for full-stack monitoring | Works together for full-stack monitoring |

**Better Together:** Use SystemMind to monitor your host system and ContainMind to monitor containers running on it!

## 🐛 Troubleshooting

### Common Issues

**Tool returns "Please run 'initialize_os_connection' first"**
- Solution: Always call `initialize_os_connection()` before using other tools

**"No result received from client-side tool execution"**
- Cause: Tool timeout or permission error
- Solution: Check permissions, try with smaller scope (e.g., limit in `find_large_files`)

**Temperature monitoring not available (Windows)**
- This is expected - Windows doesn't expose temperature sensors through standard APIs
- Use third-party tools like HWMonitor for Windows temperature monitoring

**Permission errors when scanning files**
- Normal for system directories - tool will skip inaccessible files
- Check the "permission errors" count in output

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

Built with:
- [FastMCP](https://github.com/jlowin/fastmcp) - MCP server framework
- [psutil](https://github.com/giampaolo/psutil) - Cross-platform system utilities
- [Anthropic Claude](https://www.anthropic.com/) - AI assistant integration

Special thanks to the open-source community for the excellent tools and libraries.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Ashfaqbs/SystemMind/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Ashfaqbs/SystemMind/discussions)
- **Documentation**: [Wiki](https://github.com/Ashfaqbs/SystemMind/wiki)

## 🌟 Star History

If you find SystemMind helpful, please consider giving it a star ⭐ on GitHub!

---

**SystemMind** - Making system management conversational, intelligent, and accessible to everyone. 🚀

## 💼 The Mind Suite

SystemMind is part of the **Mind Suite** - a collection of intelligent management tools:

- **🐋 [ContainMind](https://github.com/Ashfaqbs/ContainMind)** - Universal container management
- **🖥️ SystemMind** - Operating system intelligence (this project)

*From containers to OS - Mind everything.* 🧠