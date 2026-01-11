class SiteHeader extends HTMLElement {
  connectedCallback() {
    const isLanding = window.location.pathname === '/' || window.location.pathname.endsWith('/index.html') || window.location.pathname.endsWith('/jovd83_github_page/');

    // Home Icon HTML
    const homeIcon = `
      <a href="/" class="btn-icon" title="Back to Home" style="width: 32px; height: 32px;">
        <svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20">
          <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>
        </svg>
      </a>
    `;

    this.innerHTML = `
      <div class="profile-container" style="display: flex; flex-direction: row; align-items: center; justify-content: center; gap: 1rem;">
        
        <!-- Clickable Identity (Avatar + Name) -->
        <a href="/" style="display: flex; align-items: center; gap: 1rem; text-decoration: none; cursor: pointer;">
            <!-- Avatar First -->
            <img src="https://avatars.githubusercontent.com/u/116805343?v=4" alt="JOVD83" class="profile-pic" style="object-fit: cover;">

            <!-- Name Second -->
            <span class="main-title" style="font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 2.5rem; background: linear-gradient(to right, #fff, #94a3b8); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; margin: 0 0.5rem;">JOVD</span>
        </a>

        <!-- Icons Third -->
        <div class="social-links" style="display: flex; gap: 0.5rem; align-items: center;">
          <a href="https://github.com/jovd83" target="_blank" rel="noopener noreferrer" class="btn-icon" title="GitHub" style="width: 32px; height: 32px;">
            <svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20">
              <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.05-.015-2.055-3.33.72-4.035-1.605-4.035-1.605-.54-1.38-1.335-1.755-1.335-1.755-1.085-.735.09-.72.09-.72 1.2.075 1.83 1.23 1.83 1.23 1.065 1.815 2.805 1.29 3.495.99.105-.78.42-1.29.765-1.59-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405 1.02 0 2.04.135 3 .405 2.295-1.545 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.92 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.285 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z" />
            </svg>
          </a>
          <a href="https://www.linkedin.com/in/jvdorpe/" target="_blank" rel="noopener noreferrer" class="btn-icon" title="LinkedIn" style="width: 32px; height: 32px;">
            <svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20">
              <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z" />
            </svg>
          </a>
          <a href="mailto:jochimvandorpe@gmail.com" class="btn-icon" title="Email" style="width: 32px; height: 32px;">
            <svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20">
              <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
            </svg>
          </a>
          ${!isLanding ? homeIcon : ''}
        </div>
      </div>
    `;
  }
}

customElements.define('site-header', SiteHeader);
