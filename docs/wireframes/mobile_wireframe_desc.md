# Wireframe: Mobile Layout

## Core Layout Changes

### Desktop vs Mobile Comparison

| Component | Desktop View | Mobile View (< 768px) |
| :--- | :--- | :--- |
| **Hero Section** | Standard centered text | Increased padding, stacked items if necessary |
| **Navigation** | Sticky row of buttons | Sticky, horizontally scrollable row (no wrapping) |
| **Content Grid** | Multi-column grid (`repeat(auto-fill, ...))`) | Single column (`1fr`), full width cards |
| **Card Layout** | Vertical text stack | Vertical stack (unchanged layout, just width) |
| **Search Bar** | Expandable on hover | Always visible icon, expands over nav on focus OR distinct row |

## Visual Description

### Mobile View Port (390px width)

```
[ Header ]
   ( Hamburger / Brand ) --> Not strictly needed if we keep sticky nav
   AI Radar (Big Title)
   [ Profile Pic ]
   Hero Text (Centered, padded)

[ Sticky Nav ]
   < [Podcasts] [Newsletters] [Blogs] ... > (Scrollable)
   [ Search Icon ]

[ Content Section: Podcasts ]
   [ Filter: All (pill) ] [ Tech (pill) ] ...
   
   [ Card: Podcast 1 ]
   | Title           |
   | Desc...         |
   | Tags...         |
   | [Flag] [Links]  |

   [ Card: Podcast 2 ]
   ...
```

### Key Design logic
- **Touch Targets:** Minimum 44px height for all interactive elements (nav pills, filter pills).
- **Legibility:** Font size 16px minimum for body text.
- **Horizontal Scrolling:** Used for Navigation and Filter pills to save vertical space.
