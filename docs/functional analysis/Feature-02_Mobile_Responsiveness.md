# Feature: Mobile Responsiveness

## 📘 Epics & User Stories

### Epic: Mobile Experience
As a visitor to the AI Radar site, I want the website to be fully responsive and usable on my mobile device, so that I can access the content on the go.

### User Stories

#### US-01: Mobile Navigation
- **As a** mobile user
- **I want** the navigation menu to be easily accessible (e.g., sticky, horizontally scrollable, or hamburger menu)
- **So that** I can jump to different sections without excessive scrolling.

#### US-02: Readable Content
- **As a** mobile user
- **I want** the text size to be readable (at least 16px) and lines to wrap correctly
- **So that** I don't have to zoom in to read descriptions.

#### US-03: Single Column Layout
- **As a** mobile user
- **I want** the resource cards to be displayed in a single column
- **So that** they fit the screen width and I can see the details clearly.

#### US-04: Touch Friendly Targets
- **As a** mobile user
- **I want** buttons and links to be large enough to tap
- **So that** I don't accidentally click the wrong item.

#### US-05: Hero Section Adaptation
- **As a** mobile user
- **I want** the hero section (title and bio) to stack vertically if needed and have appropriate padding
- **So that** it looks professional and doesn't waste screen space.

### Acceptance Criteria
1.  **Layout:**
    - The grid layout switches to a single column on devices narrower than 768px.
    - No horizontal scrolling is triggered by overflowing elements.
2.  **Navigation:**
    - The navigation bar is sticky and allows access to all items (e.g., via horizontal scroll).
    - Search input expands correctly without breaking the layout.
3.  **Typography:**
    - Base font size is legible.
    - Headings are scaled down appropriately to fit the screen.
4.  **Desktop Regression:**
    - The desktop view (screens > 1024px) remains pixel-perfectly identical to the previous version.
