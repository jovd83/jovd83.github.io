# CR-01: Split AI Activities Board & Enhance Cards

## 1. Overview
This change request splits the monolithic "AI Activities" board into distinct, categorized sections (Podcasts, Newsletters, Blogs, YouTube, Courses, Tools). It also improves content discovery by adding "Intro Phrases" to each section, subcategory-based filtering within sections, and richer card metadata (hosts, vendors, platform logos).

## 2. Impacted User Stories
*   **US-01 [Refined]:** As a user, I want to view my AI resources organized by specific category (Podcast, Newsletter, etc.) in separate vertical sections so that I can focus on one type of content at a time.
    *   *Old Behavior:* All content mixed in one grid with a global filter.
    *   *New Behavior:* Vertical scrollable page with distinct headers and grids for each category.
*   **US-02 [Refined]:** As a user, I want to filter content within a category by "subcategory" so that I can find specific topics (e.g., "Coding" vs "Marketing" in YouTube).
*   **US-03 [Refined]:** As a user, I want to see specific details relevant to the content type (e.g., Host for podcasts, Vendor for tools) to better understand the resource.
*   **US-04 [Refined]:** As a user, I want to easily access content on its native platform (Apple Podcasts, Spotify, YouTube) via recognizable icons.

## 3. Functional Requirements

### 3.1. Layout
*   The application shall display the following sections in order:
    1.  Podcasts
    2.  Newsletters
    3.  Blogs (New)
    4.  YouTube Channels
    5.  Courses
    6.  Tools
*   Each section shall have a Header containing:
    *   Title (e.g., "Podcasts")
    *   Intro Phrase (e.g., "Listen to the latest AI discussions...")
    *   Subcategory Filter Pills (dynamically generated from columns).

### 3.2. Data & Content
*   **Podcasts**: Display "Host: [Name]". Show Apple/Spotify logo buttons if links exist.
*   **Newsletters**: Display "Provided by: [Name]".
*   **Blogs**: New category. Display standard card info.
*   **YouTube**: Display YouTube logo button for the link.
*   **Courses**: Display "Provided by: [Name]".
*   **Tools**: Display "Vendor: [Name]".

### 3.3. Filtering
*   Clicking a subcategory pill (e.g., "Dev") in the "Tools" section shall only filter the cards in the "Tools" section.
*   "All" pill shall be selected by default in each section.

## 4. Technical Constraints
*   Data must continue to be loaded from CSVs in `public/data/`.
*   No database backend; purely client-side parsing.
*   Must maintain responsive design.
