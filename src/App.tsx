import { useEffect, useState } from 'react';
import Papa from 'papaparse';
import './App.css';
import './components/SiteHeader.js';

// --- Types ---
interface ContentItem {
  title: string;
  description: string;
  tags?: string; // Optional now as strictly typed
  Frequency?: string; // New column from podcasts.csv
  link_primary: string;
  link_secondary?: string; // Generic secondary link (kept for backward compat or flexible use)
  image_url?: string;
  category: ContentType; // Added purely for internal state management

  // New fields
  subcategory?: string;
  host?: string;
  provided_by?: string; // For Newsletters / Courses
  vendor?: string; // For Tools
  country?: string; // New: Country of origin
  use_cases?: string; // New: My use cases
  apple_podcasts_link?: string;
  spotify_podcasts_link?: string;
  youtube_podcast_link?: string;
}

type ContentType = 'Podcasts' | 'Newsletters' | 'Blogs' | 'YouTube' | 'Courses' | 'Tools' | 'Benchmarks' | 'Libraries' | 'Prompt Frameworks';

// --- Helper Functions ---
const parseList = (str: string | undefined): string[] => {
  if (!str) return [];
  // Remove brackets [ ] and split by comma
  const cleaned = str.replace(/[\[\]]/g, '');
  return cleaned.split(',').map(s => s.trim()).filter(s => s.length > 0);
};

// Helper: Get color class for a tag
// Using a simple hash-like approach or predefined map for common tags
const getTagColorClass = (tag: string): string => {
  const lower = tag.toLowerCase();

  if (lower.includes('coding') || lower.includes('dev') || lower.includes('mcp')) return 'tag-blue';
  if (lower.includes('ai') || lower.includes('llm') || lower.includes('prompts')) return 'tag-purple';
  if (lower.includes('news') || lower.includes('red')) return 'tag-red'; // Fixed: 'news' -> 'tag-red'
  if (lower.includes('design') || lower.includes('creative')) return 'tag-pink';
  if (lower.includes('edu') || lower.includes('tutorial') || lower.includes('skills')) return 'tag-green';
  if (lower.includes('product') || lower.includes('tool')) return 'tag-orange';

  return ''; // Default (grey)
};

// Helper: Get Country Code for FlagCDN
const getCountryCode = (country: string | undefined): string => {
  if (!country) return '';
  const lower = country.toLowerCase();

  if (lower.includes('usa') || lower.includes('united states') || lower.includes('us')) return 'us';
  if (lower.includes('uk') || lower.includes('united kingdom') || lower.includes('britain')) return 'gb';
  if (lower.includes('france')) return 'fr';
  if (lower.includes('germany')) return 'de';
  if (lower.includes('canada')) return 'ca';
  if (lower.includes('australia')) return 'au';
  if (lower.includes('china')) return 'cn';
  if (lower.includes('india')) return 'in';
  if (lower.includes('israel')) return 'il';
  if (lower.includes('czech')) return 'cz';
  if (lower.includes('switzer')) return 'ch';
  if (lower.includes('netherland')) return 'nl';
  if (lower.includes('belgium')) return 'be';
  if (lower.includes('singapore')) return 'sg';

  return '';
};

// --- Data Fetching Hook ---
const useCSVData = (fileName: string, category: ContentType) => {
  const [data, setData] = useState<ContentItem[]>([]);

  useEffect(() => {
    Papa.parse(`/data/${fileName}`, {
      download: true,
      header: true,
      skipEmptyLines: true,
      complete: (results) => {
        console.log(`Parsed ${fileName}:`, results); // Debug logging
        if (results.errors && results.errors.length > 0) {
          console.error(`Errors parsing ${fileName}:`, results.errors);
        }
        const items = (results.data as any[]).map(raw => ({
          ...raw,
          title: raw.Title || raw.title || raw.Name, // Added raw.Name
          description: raw.Description || raw.description,
          tags: raw.Tags || raw.tags,
          subcategory: raw.Subcategory || raw.subcategory,
          host: raw.Host || raw.host,
          provided_by: raw.provided_by, // Explicit map
          vendor: raw.vendor, // Explicit map
          // Map new columns 
          use_cases: raw["My use cases for it"] || raw["When to use it"], // Added raw["When to use it"]
          country: raw["country of origin"],
          // Map Website URL for tools (or generic link)
          link_primary: raw["Website URL"] || raw.link_primary || raw.Link || raw.URL || raw["URL to explanation"],
          category,
        })).filter(item => item.title); // Basic validation
        console.log(`Loaded ${items.length} items for ${category}`);
        setData(items);
      },
      error: (err) => console.error(`Error loading ${fileName}:`, err)
    });
  }, [fileName, category]);

  return data;
};

// --- Components ---

// Updated Card props to include onTagClick
function Card({ item, index, onTagClick }: { item: ContentItem; index: number; onTagClick: (tag: string) => void }) {
  const isPodcast = item.category === 'Podcasts';
  const isYoutube = item.category === 'YouTube';

  // Parse tags using true list parsing
  // Support both 'tags' and 'Frequency' (new podcasts column)
  const tagSource = item.tags || item.Frequency;
  const tags = parseList(tagSource);

  return (
    <div
      className="card"
      style={{ animationDelay: `${index * 0.05}s` } as React.CSSProperties} // Staggered animation
    >
      <div className="card-top">
        {item.image_url ?
          <img src={item.image_url} alt={item.title} className="card-img" onError={(e) => (e.currentTarget.style.display = 'none')} />
          : <div className="card-placeholder">{item.title[0]}</div>
        }
      </div>
      <div className="card-content">
        <h3>{item.title}</h3>

        {/* Metadata: Host / Provided By / Vendor */}
        {item.host && <p className="card-meta"><strong>Host:</strong> {item.host}</p>}
        {item.provided_by && <p className="card-meta"><strong>Provided by:</strong> {item.provided_by}</p>}
        {item.vendor && <p className="card-meta"><strong>Vendor:</strong> {item.vendor}</p>}

        <p className="card-desc">{item.description}</p>

        {/* Use Cases (Specific to Tools) */}
        {item.use_cases && (
          <div className="card-use-cases" style={{ marginBottom: '1rem', fontSize: '0.85rem', color: '#cbd5e1', fontStyle: 'italic', borderLeft: '2px solid var(--accent-color)', paddingLeft: '0.5rem' }}>
            <span style={{ marginRight: '0.3rem' }}>💡</span>
            {item.use_cases}
          </div>
        )}

        <div className="card-tags">
          {tags.map((tag, i) => (
            <span
              key={i}
              className={`tag ${getTagColorClass(tag)}`}
              onClick={() => onTagClick(tag)}
              style={{ cursor: 'pointer' }}
              title={`Filter by ${tag}`}
            >
              {tag}
            </span>
          ))}
        </div>
      </div>

      <div className="card-actions" style={{ justifyContent: 'space-between' }}>
        {/* Left Side: Country Flag */}
        <div className="card-action-left" style={{ display: 'flex', alignItems: 'center' }}>
          {item.country && (
            <div title={item.country} style={{ display: 'flex', alignItems: 'center' }}>
              {(() => {
                const code = getCountryCode(item.country);
                return code ? (
                  <img
                    src={`https://flagcdn.com/w40/${code}.png`}
                    srcSet={`https://flagcdn.com/w80/${code}.png 2x`}
                    width="24"
                    height="16"
                    alt={item.country}
                    style={{ borderRadius: '2px', objectFit: 'cover' }}
                  />
                ) : (
                  <span style={{ fontSize: '1.2rem' }}>🏳️</span>
                );
              })()}
            </div>
          )}
        </div>

        {/* Right Side: Links */}
        <div className="card-action-right" style={{ display: 'flex', gap: '0.75rem' }}>
          {/* Primary Link (Generic) - Hide for Podcasts if they have specific links (User Request) */}
          {item.link_primary && !isYoutube && !isPodcast && (
            <a href={item.link_primary} target="_blank" rel="noopener noreferrer" className="btn-icon" title="Visit Website">
              🌐
            </a>
          )}

          {/* YouTube Link / Channel - For YouTube Category */}
          {isYoutube && item.link_primary && (
            <a href={item.link_primary} target="_blank" rel="noopener noreferrer" className="btn-icon youtube-btn" title="Watch on YouTube">
              <svg viewBox="0 0 24 24" fill="currentColor" width="24" height="24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z" /></svg>
            </a>
          )}

          {/* Podcast Specific Links */}
          {item.apple_podcasts_link && (
            <a href={item.apple_podcasts_link} target="_blank" rel="noopener noreferrer" className="btn-icon apple-btn" title="Apple Podcasts">
              <svg viewBox="0 0 24 24" fill="currentColor" width="24" height="24"><path d="M5.34 0A5.328 5.328 0 000 5.34v13.32A5.328 5.328 0 005.34 24h13.32A5.328 5.328 0 0024 18.66V5.34A5.328 5.328 0 0018.66 0zm6.525 2.568c2.336 0 4.448.902 6.056 2.587 1.224 1.272 1.912 2.619 2.264 4.392.12.59.12 2.2.007 2.864a8.506 8.506 0 01-3.24 5.296c-.608.46-2.096 1.261-2.336 1.261-.088 0-.096-.091-.056-.46.072-.592.144-.715.48-.856.536-.224 1.448-.874 2.008-1.435a7.644 7.644 0 002.008-3.536c.208-.824.184-2.656-.048-3.504-.728-2.696-2.928-4.792-5.624-5.352-.784-.16-2.208-.16-3 0-2.728.56-4.984 2.76-5.672 5.528-.184.752-.184 2.584 0 3.336.456 1.832 1.64 3.512 3.192 4.512.304.2.672.408.824.472.336.144.408.264.472.856.04.36.03.464-.056.464-.056 0-.464-.176-.896-.384l-.04-.03c-2.472-1.216-4.056-3.274-4.632-6.012-.144-.706-.168-2.392-.03-3.04.36-1.74 1.048-3.1 2.192-4.304 1.648-1.737 3.768-2.656 6.128-2.656zm.134 2.81c.409.004.803.04 1.106.106 2.784.62 4.76 3.408 4.376 6.174-.152 1.114-.536 2.03-1.216 2.88-.336.43-1.152 1.15-1.296 1.15-.023 0-.048-.272-.048-.603v-.605l.416-.496c1.568-1.878 1.456-4.502-.256-6.224-.664-.67-1.432-1.064-2.424-1.246-.64-.118-.776-.118-1.448-.008-1.02.167-1.81.562-2.512 1.256-1.72 1.704-1.832 4.342-.264 6.222l.413.496v.608c0 .336-.027.608-.06.608-.03 0-.264-.16-.512-.36l-.034-.011c-.832-.664-1.568-1.842-1.872-2.997-.184-.698-.184-2.024.008-2.72.504-1.878 1.888-3.335 3.808-4.019.41-.145 1.133-.22 1.814-.211zm-.13 2.99c.31 0 .62.06.844.178.488.253.888.745 1.04 1.259.464 1.578-1.208 2.96-2.72 2.254h-.015c-.712-.331-1.096-.956-1.104-1.77 0-.733.408-1.371 1.112-1.745.224-.117.534-.176.844-.176zm-.011 4.728c.988-.004 1.706.349 1.97.97.198.464.124 1.932-.218 4.302-.232 1.656-.36 2.074-.68 2.356-.44.39-1.064.498-1.656.288h-.003c-.716-.257-.87-.605-1.164-2.644-.341-2.37-.416-3.838-.218-4.302.262-.616.974-.966 1.97-.97z" /></svg>
            </a>
          )}
          {item.spotify_podcasts_link && (
            <a href={item.spotify_podcasts_link} target="_blank" rel="noopener noreferrer" className="btn-icon spotify-btn" title="Spotify">
              <svg viewBox="0 0 24 24" fill="currentColor" width="24" height="24"><path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.717.476-1.076.236-2.964-1.811-6.696-2.22-11.093-1.217-.417.095-.826-.167-.921-.583-.095-.417.167-.826.583-.921 4.793-1.09 8.914-.623 12.27 1.417.36.24.477.718.237 1.068zm1.533-3.414c-.302.494-.93.645-1.424.353-3.39-2.085-8.567-2.688-12.583-1.472-.559.171-1.144-.144-1.314-.703-.171-.559.144-1.144.703-1.314 4.586-1.385 10.324-.706 14.265 1.745.495.302.646.931.353 1.391zm.146-3.473C15.158 8.169 8.799 7.979 5.122 9.096c-.66.2-1.378-.179-1.578-.839-.2-.66.179-1.378.839-1.578 4.296-1.304 11.365-1.082 16.035 1.691.595.353.791 1.12.438 1.714-.352.595-1.12.791-1.714.438z" /></svg>
            </a>
          )}
          {item.youtube_podcast_link && (
            <a href={item.youtube_podcast_link} target="_blank" rel="noopener noreferrer" className="btn-icon youtube-btn" title="Watch on YouTube">
              <svg viewBox="0 0 24 24" fill="currentColor" width="24" height="24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z" /></svg>
            </a>
          )}

          {/* Keep generic secondary for backward compat or other uses */}
          {item.link_secondary && !isPodcast && (
            <a href={item.link_secondary} target="_blank" rel="noopener noreferrer" className="btn-icon" title="Secondary Link">
              🎧
            </a>
          )}
        </div>
      </div>
    </div>
  );
}

// --- Section Component ---

interface SectionProps {
  title: string;
  intro: string;
  data: ContentItem[];
  id: string;
}

// Helper for icons (simple SVGs as constants to keep JSX clean)
const IconGrid = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
);

const IconList = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></svg>
);

const IconDownload = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
);


function Section({ title, intro, data, id }: SectionProps) {
  const [filter, setFilter] = useState('All');
  const [sortOrder, setSortOrder] = useState('Default');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  // Collapse state
  const [isCollapsed, setIsCollapsed] = useState(false);

  // Initialize collapse state based on viewport width
  useEffect(() => {
    const handleResize = () => {
      // If mobile (< 768px), collapse by default
      if (window.innerWidth < 768) {
        setIsCollapsed(true);
      } else {
        setIsCollapsed(false);
      }
    };

    // Run once on mount
    handleResize();
  }, []);

  // Derive counts for subcategories
  const subcategoryCounts = data.reduce((acc, item) => {
    const subs = parseList(item.subcategory);
    subs.forEach(sub => {
      if (!acc[sub]) acc[sub] = 0; // Initialize key
    });
    return acc;
  }, {} as Record<string, number>);

  // 2. Calculate counts for each unique subcategory
  Object.keys(subcategoryCounts).forEach(subKey => {
    subcategoryCounts[subKey] = data.filter(d => {
      const dSubs = parseList(d.subcategory);
      const dTags = parseList(d.tags || d.Frequency);
      return dSubs.includes(subKey) || dTags.includes(subKey);
    }).length;
  });

  const subcategories = Object.keys(subcategoryCounts).sort();
  const hasSubcategories = subcategories.length > 0;

  // Filter Logic
  const filteredData = filter === 'All'
    ? data
    : data.filter(d => {
      const subs = parseList(d.subcategory);
      const tags = parseList(d.tags || d.Frequency);
      return subs.includes(filter) || tags.includes(filter);
    });

  // Sorting Logic
  const sortedData = [...filteredData].sort((a, b) => {
    if (sortOrder === 'A-Z') return a.title.localeCompare(b.title);
    if (sortOrder === 'Z-A') return b.title.localeCompare(a.title);

    if (sortOrder === 'Subcategory') {
      const subA = (a.subcategory || '').toLowerCase();
      const subB = (b.subcategory || '').toLowerCase();
      const cmp = subA.localeCompare(subB);
      if (cmp !== 0) return cmp;
      return a.title.localeCompare(b.title);
    }

    if (sortOrder === 'Vendor') {
      const vA = (a.vendor || a.host || '').toLowerCase();
      const vB = (b.vendor || b.host || '').toLowerCase();
      const cmp = vA.localeCompare(vB);
      if (cmp !== 0) return cmp;
      return a.title.localeCompare(b.title);
    }

    if (sortOrder === 'Country') {
      const cA = (a.country || '').toLowerCase();
      const cB = (b.country || '').toLowerCase();
      const cmp = cA.localeCompare(cB);
      if (cmp !== 0) return cmp;
      return a.title.localeCompare(b.title);
    }

    return 0; // Default
  });

  const handleExportCSV = () => {
    const csv = Papa.unparse(data);
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `${title.replace(/\s+/g, '_')}_export.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  if (data.length === 0) return null;

  return (
    <section id={id} className={`content-section ${id}-section`}>
      <header className="section-header">
        <div style={{ marginBottom: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flexWrap: 'wrap', marginBottom: '0.5rem' }}>

            {/* Title with Toggle */}
            <h2
              style={{ margin: 0, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.5rem' }}
              onClick={() => setIsCollapsed(!isCollapsed)}
              title={isCollapsed ? "Expand Section" : "Collapse Section"}
            >
              {title}
              <span style={{ fontSize: '1.2rem', transform: isCollapsed ? 'rotate(-90deg)' : 'rotate(0deg)', transition: 'transform 0.3s ease', display: 'inline-block' }}>
                ▼
              </span>
            </h2>

            {!isCollapsed && (
              <div className="section-controls" style={{ display: 'flex', gap: '0.5rem', alignItems: 'center', marginLeft: 'auto' }}>
                <select
                  className="sort-select"
                  value={sortOrder}
                  onChange={(e) => setSortOrder(e.target.value)}
                  title="Sort Order"
                >
                  <option value="Default">Default</option>
                  <option value="A-Z">A-Z</option>
                  <option value="Z-A">Z-A</option>
                  <option value="Subcategory">Subcategory</option>
                  {title === 'Tools' && (
                    <>
                      <option value="Vendor">Vendor</option>
                      <option value="Country">Country</option>
                    </>
                  )}
                </select>

                <button
                  className="toggle-btn"
                  onClick={handleExportCSV}
                  title="Export to CSV"
                >
                  <IconDownload />
                </button>

                <div className="view-toggle">
                  <button
                    className={`toggle-btn ${viewMode === 'grid' ? 'active' : ''}`}
                    onClick={() => setViewMode('grid')}
                    title="Grid View"
                  >
                    <IconGrid />
                  </button>
                  <button
                    className={`toggle-btn ${viewMode === 'list' ? 'active' : ''}`}
                    onClick={() => setViewMode('list')}
                    title="List View"
                  >
                    <IconList />
                  </button>
                </div>
              </div>
            )}
          </div>

          {!isCollapsed && <p className="intro-phrase">{intro}</p>}
        </div>

        {!isCollapsed && (hasSubcategories || filter !== 'All') && (
          <div className="section-filter-bar">
            <button
              className={`filter-pill ${filter === 'All' ? 'active-pill' : ''}`}
              onClick={() => setFilter('All')}
            >
              All ({data.length})
            </button>

            {subcategories.map(sub => (
              <button
                key={sub}
                className={`filter-pill ${filter === sub ? 'active-pill' : ''}`}
                onClick={() => setFilter(sub)}
              >
                {sub} ({subcategoryCounts[sub]})
              </button>
            ))}

            {filter !== 'All' && !subcategories.includes(filter) && (
              <button
                className="filter-pill active-pill custom-tag-filter"
                onClick={() => setFilter('All')}
                title="Clear Tag Filter"
                style={{ border: '1px dashed var(--accent-color)' }}
              >
                🏷️ {filter} ✕
              </button>
            )}
          </div>
        )}
      </header>

      {!isCollapsed && (
        <div className={`scroll-pane ${viewMode === 'list' ? 'list-view' : ''}`}>
          {sortedData.map((item, idx) => (
            <Card
              key={`${title}-${item.title}-${idx}`}
              item={item}
              index={idx}
              onTagClick={setFilter}
            />
          ))}
        </div>
      )}
    </section>
  )
}


function App() {
  const podcasts = useCSVData('podcasts.csv', 'Podcasts');
  const newsletters = useCSVData('newsletters.csv', 'Newsletters');
  const blogs = useCSVData('blogs.csv', 'Blogs');
  const youtube = useCSVData('youtube.csv', 'YouTube');
  const courses = useCSVData('courses.csv', 'Courses');
  const tools = useCSVData('tools.csv', 'Tools');
  const benchmarks = useCSVData('benchmarks.csv', 'Benchmarks');
  const libraries = useCSVData('libraries.csv', 'Libraries');
  const frameworks = useCSVData('prompt_frameworks.csv', 'Prompt Frameworks' as any); // Cast as any or update type

  // New State: Search
  const [searchTerm, setSearchTerm] = useState('');
  // New State: Scroll Button
  const [showTopBtn, setShowTopBtn] = useState(false);

  // Scroll Listener
  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 400) {
        setShowTopBtn(true);
      } else {
        setShowTopBtn(false);
      }
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // New: Global Filter Logic
  const filterBySearch = (items: ContentItem[]) => {
    if (!searchTerm) return items;
    const lower = searchTerm.toLowerCase();
    return items.filter(item =>
      item.title.toLowerCase().includes(lower) ||
      item.description.toLowerCase().includes(lower) ||
      (item.tags && item.tags.toLowerCase().includes(lower))
    );
  };

  // Intro Phrases
  const intros = {
    Podcasts: "These are the shows I listen to during commutes, while preparing dinner, or while walking outdoors. They help me absorb AI developments in a conversational format, often featuring practitioners who share real-world experiences and insights you won't find in press releases. I pick episodes based on guests and topics rather than listening to everything, except for 'The AI Daily Brief', which I listen to six times a week.",
    Newsletters: "My curated inbox of AI updates that I actually read. These newsletters cut through the noise and deliver the signal, whether it's breaking research, practical applications, or industry trends. They save me hours of scrolling and help me start each week knowing what matters.",
    Blogs: "The deeper dives I turn to when I want to understand how something actually works. These blogs go beyond the headlines to explain architectures, share implementation details, and explore the implications of new developments. They're my go-to when a mention, a news article, or a podcast item leaves me wanting more.",
    YouTube: "Visual learning works for me, especially for tutorials and technical explanations. These channels help me understand complex concepts through demonstrations, code walkthroughs, and visual breakdowns that text alone can't convey. I watch selectively—I scroll through my subscription page and add those I'm interested in to my 'Watch later' watchlist.",
    Courses: "The structured learning I've invested time in when I wanted to build foundational knowledge or level up specific skills. Not everything needs a course, but these have been worth the time commitment when I needed more than just surface-level understanding.",
    Tools: "The AI applications I actually use (or used) in my workflow. Some tools have earned a permanent spot in how I work, research, or experiment; others have in the meantime already been replaced. The list evolves as new tools prove their value and others fade away.",
    Benchmarks: "The scorecards I check when evaluating models or understanding capabilities. Benchmarks aren't perfect, but they provide useful reference points for comparing models and tracking progress. I use these to inform decisions, not to make them for me.",
    "Prompt Frameworks": "The patterns and structures I rely on when crafting prompts. These frameworks help me get better results more consistently, whether I'm prototyping something new or refining a production workflow. They're mental models that have proven useful across different models and use cases.",
    Libraries: "Curated collections of prompts, tools, and resources that I reference to save time and discover new capabilities. These repositories are great starting points when I need inspiration or want to see how others are solving specific problems."
  };

  const navItems = [
    { id: 'podcasts', label: 'Podcasts', count: podcasts.length },
    { id: 'newsletters', label: 'Newsletters', count: newsletters.length },
    { id: 'blogs', label: 'Blogs', count: blogs.length },
    { id: 'youtube', label: 'YouTube', count: youtube.length },
    { id: 'courses', label: 'Courses', count: courses.length },
    { id: 'tools', label: 'Tools', count: tools.length },
    { id: 'benchmarks', label: 'Benchmarks', count: benchmarks.length },
    { id: 'libraries', label: 'Libraries', count: libraries.length },
    { id: 'frameworks', label: 'Frameworks', count: frameworks.length },
  ];

  const scrollToSection = (id: string) => {
    const element = document.getElementById(id);
    if (element) {
      // Offset for sticky nav height (approx 80px)
      const y = element.getBoundingClientRect().top + window.scrollY - 100;
      window.scrollTo({ top: y, behavior: 'smooth' });
    }
  };



  return (
    <div className="app-container">
      <header className="hero">
        {/* @ts-ignore */}
        <site-header></site-header>
        <h1 className="main-title">AI Radar</h1>
        <div className="hero-content">
          <img src="/img/thumbs/radar.png" alt="AI Radar" className="hero-image" />
          <p className="bio">
            People often ask me where I get my AI information, which models I use, and how I stay current in this fast-moving field. This page is my personal AI radar: not an exhaustive list, but simply the resources and tools that have become part of my daily routine, both in my professional life and for my hobbies. Your mileage may vary, and there are plenty of other great options out there. Consider this a starting point for building your own AI toolkit, shaped by what works for your specific needs and interests.
          </p>
        </div>
      </header>

      <nav className="sticky-nav">
        <ul className="nav-list">
          {navItems.map(item => (
            <li key={item.id}>
              {/* Only show nav items if they are populated */}
              {item.count > 0 && (
                <button onClick={() => scrollToSection(item.id)} className="nav-link">
                  {item.label}
                </button>
              )}
            </li>
          ))}
        </ul>

        {/* Search Bar */}
        <div className="search-container">
          <span style={{ fontSize: '1.2rem' }}>🔍</span>
          <input
            type="text"
            placeholder="Search radar..."
            className="search-input"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </nav>

      <main className="main-content-stack">
        <Section id="podcasts" title="Podcasts" intro={intros.Podcasts} data={filterBySearch(podcasts)} />
        <Section id="newsletters" title="Newsletters" intro={intros.Newsletters} data={filterBySearch(newsletters)} />
        <Section id="blogs" title="Blogs" intro={intros.Blogs} data={filterBySearch(blogs)} />
        <Section id="youtube" title="YouTube Channels" intro={intros.YouTube} data={filterBySearch(youtube)} />
        <Section id="courses" title="Courses" intro={intros.Courses} data={filterBySearch(courses)} />
        <Section id="tools" title="Tools" intro={intros.Tools} data={filterBySearch(tools)} />
        <Section id="benchmarks" title="Benchmarks & Reports" intro={intros.Benchmarks} data={filterBySearch(benchmarks)} />
        <Section id="libraries" title="Libraries" intro={intros.Libraries} data={filterBySearch(libraries)} />
        <Section id="frameworks" title="Prompt Frameworks" intro={intros["Prompt Frameworks"]} data={filterBySearch(frameworks)} />
      </main>

      <div style={{ textAlign: 'center', margin: '4rem 0' }}>
        <a href="/" className="back-link">← Back to Home</a>
      </div>



      {/* Back to Top Button */}
      <div className={`back-to-top ${showTopBtn ? 'visible' : ''}`} onClick={scrollToTop}>
        ↑
      </div>
    </div>
  );
}

export default App;
