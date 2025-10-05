# Grove TUI Roadmap

## Vision

Grove will have two complementary interfaces:

1. **CLI (Current)** - Streamlined, focused on core operations
2. **TUI (Future)** - Interactive terminal interface for complex workflows

## CLI vs TUI Feature Distribution

### CLI Features (Core Operations)
*Simple, scriptable operations that work well in pipelines*

✅ **Current CLI Features:**
- Basic course listing and filtering
- Major-based filtering (EE, CpE, CS, IT, etc.)
- Academic level filtering (undergraduate/graduate)  
- Course statistics generation
- CSV export functionality
- Course history integration with eligibility status
- Prerequisite display with logical AND/OR relationships
- Verbose detailed output mode

### TUI Features (Interactive Operations)
*Complex, multi-step workflows that benefit from interactivity*

🚧 **Planned TUI Features:**
- **Interactive Search** - Real-time search with filtering and highlighting
- **Prerequisite Chain Visualization** - Visual prerequisite trees and dependency graphs  
- **Path Planning** - Interactive course sequence planning to reach target courses
- **Course Comparison** - Side-by-side course comparison interface
- **Advanced Filtering** - Multi-criteria filtering with live preview
- **Course Recommendations** - AI-powered course suggestions based on interests/goals
- **Progress Tracking** - Visual degree progress with completion percentages
- **Interactive Prerequisites** - Click-to-explore prerequisite relationships
- **Curriculum Planning** - Semester-by-semester course planning interface
- **Export Wizard** - Guided export with custom formatting options

## Technical Architecture

### CLI Implementation
- **Language:** Python 3.7+
- **Dependencies:** PyMuPDF for PDF parsing
- **Interface:** Standard argparse CLI
- **Output:** Formatted text with color support
- **Export:** CSV format

### TUI Implementation (Planned)
- **Framework:** Rich/Textual for modern TUI interface
- **Data Layer:** Shared parsing engine with CLI
- **State Management:** Session-based workflow state
- **Navigation:** Tab-based interface with keyboard shortcuts
- **Search:** Real-time filtering with fuzzy matching
- **Visualization:** ASCII graphs and trees for prerequisites

## Development Phases

### Phase 1: CLI Foundation ✅
- [x] Core PDF parsing functionality
- [x] Basic filtering and display
- [x] Prerequisite parsing with logical relationships
- [x] CSV export
- [x] Grove branding and professional output

### Phase 2: CLI Polish (Current)
- [x] Remove complex features to simplify CLI
- [x] Improve output formatting and colors
- [x] Add comprehensive documentation
- [ ] Create installation script
- [ ] Add shell completion

### Phase 3: TUI Planning (Next)
- [ ] Research TUI frameworks (Rich vs Textual)
- [ ] Design TUI interface mockups
- [ ] Plan shared data architecture
- [ ] Create TUI feature specifications

### Phase 4: TUI Development (Future)
- [ ] Build core TUI framework
- [ ] Implement interactive search
- [ ] Add prerequisite visualization
- [ ] Build course planning interface
- [ ] Add progress tracking features

### Phase 5: Integration (Future)
- [ ] Shared configuration system
- [ ] Data export between CLI/TUI
- [ ] Unified documentation
- [ ] Cross-platform testing

## Design Principles

### CLI Design
- **Simplicity** - Each operation should do one thing well
- **Composability** - Output should work with other CLI tools
- **Speed** - Fast startup and execution for quick queries
- **Scriptability** - Easy to use in automation and pipelines

### TUI Design  
- **Discoverability** - Features should be easy to find and learn
- **Efficiency** - Power users should be able to work quickly
- **Visual** - Complex relationships should be visualized clearly
- **Stateful** - Should remember user context and preferences

## Migration Strategy

1. **No Breaking Changes** - CLI will maintain compatibility
2. **Feature Flag System** - Gradual TUI rollout with feature flags
3. **Documentation** - Clear guidance on when to use CLI vs TUI
4. **User Choice** - Both interfaces will remain fully supported

## Success Metrics

### CLI Success
- Fast execution (< 1 second for most operations)
- Clear, parseable output
- Comprehensive documentation
- Easy installation and setup

### TUI Success  
- Interactive workflows complete 3x faster than CLI equivalents
- Visual prerequisite trees improve understanding
- Course planning reduces scheduling conflicts
- User adoption for complex analysis tasks

---

*This roadmap will be updated as development progresses and user feedback is incorporated.*