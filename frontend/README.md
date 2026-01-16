# Talk-Less Frontend

This is the frontend application for Talk-Less, a transparent multi-perspective news aggregation platform.

## Technology Stack

- **React 18**: Modern React with functional components and hooks
- **React Router 6**: Client-side routing
- **CSS3**: Responsive, accessible styling with CSS custom properties
- **Fetch API**: Backend communication

## Prerequisites

- Node.js 14+ and npm
- Backend API running (default: http://localhost:8000)

## Setup

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment (optional):**
   Create a `.env` file to override default API URL:
   ```
   REACT_APP_API_URL=http://localhost:8000
   ```

3. **Start development server:**
   ```bash
   npm start
   ```
   
   Opens at http://localhost:3000 with hot reloading.

4. **Build for production:**
   ```bash
   npm run build
   ```
   
   Creates optimized build in `build/` directory.

## Project Structure

```
frontend/
├── public/
│   ├── index.html          # HTML entry point
│   └── manifest.json       # PWA manifest
├── src/
│   ├── components/
│   │   ├── Header.js       # Navigation header
│   │   ├── Footer.js       # Site footer
│   │   ├── SummaryList.js  # News summaries list
│   │   ├── SummaryDetail.js # Individual summary view
│   │   ├── SourceList.js   # News sources page
│   │   ├── BiasIndicators.js # Bias visualization
│   │   ├── About.js        # About page
│   │   ├── Transparency.js # Transparency page
│   │   └── NotFound.js     # 404 page
│   ├── App.js              # Main app component
│   ├── App.css             # Global styles
│   └── index.js            # React entry point
├── package.json
└── README.md
```

## Features

### Core Pages

- **Home (`/`)**: List of latest news summaries with pagination
- **Summary Detail (`/summary/:id`)**: Full summary with sources and bias indicators
- **Sources (`/sources`)**: List of all news sources with methodology
- **About (`/about`)**: Project mission and principles
- **Transparency (`/transparency`)**: Complete methodology documentation

### Key Features

- **Responsive Design**: Works on mobile, tablet, and desktop
- **Accessibility**: WCAG 2.1 AA compliant
  - Semantic HTML
  - ARIA labels
  - Keyboard navigation
  - Screen reader support
- **No Tracking**: Zero analytics, cookies, or user profiling
- **Progressive Enhancement**: Works without JavaScript (static HTML)
- **Performance**: Lazy loading, code splitting, optimized assets

### Design Principles

1. **Minimalist**: Clean, distraction-free interface
2. **Transparent**: Clear source attribution and bias indicators
3. **Accessible**: Usable by everyone, including assistive technology users
4. **Privacy-Focused**: No tracking, analytics, or user profiling
5. **Responsive**: Adapts to all screen sizes

## API Integration

The frontend communicates with the backend API:

- **Base URL**: `process.env.REACT_APP_API_URL` or `http://localhost:8000`
- **Endpoints Used**:
  - `GET /api/summaries` - List summaries (with pagination)
  - `GET /api/summaries/:id` - Get summary details
  - `GET /api/sources` - List news sources
  - `GET /api/health` - Health check

### Error Handling

- Network errors show user-friendly messages
- Failed requests display retry buttons
- Loading states prevent confusion
- 404s redirect to NotFound page

## Development

### Available Scripts

- `npm start` - Development server with hot reload
- `npm run build` - Production build
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App (irreversible)

### Code Style

- Functional components with hooks
- PropTypes for type checking
- CSS modules for component styles
- Semantic HTML5 elements
- Accessible markup (ARIA, alt text, labels)

### Adding New Components

1. Create component file in `src/components/`
2. Add corresponding CSS file
3. Include AGPL license header
4. Export from component file
5. Import in `App.js` and add route if needed

## Deployment

### Static Hosting

Build and deploy to any static host:

```bash
npm run build
# Deploy contents of build/ directory
```

Supports: Netlify, Vercel, GitHub Pages, AWS S3, etc.

### Docker

Include frontend build in backend Docker image:

```dockerfile
# Build frontend
FROM node:18 AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Add to backend image
COPY --from=frontend-build /app/frontend/build /app/frontend/build
```

### Environment Variables

- `REACT_APP_API_URL`: Backend API base URL
- `NODE_ENV`: `production` for optimized builds

## Browser Support

- Chrome/Edge (last 2 versions)
- Firefox (last 2 versions)
- Safari (last 2 versions)
- iOS Safari (last 2 versions)
- Android Chrome (last 2 versions)

## Accessibility

Complies with WCAG 2.1 Level AA:

- Semantic HTML structure
- Sufficient color contrast (4.5:1 minimum)
- Keyboard navigation support
- Screen reader compatibility
- Focus indicators
- Skip to main content link
- ARIA labels and roles

Test with:
- Screen readers (NVDA, JAWS, VoiceOver)
- Keyboard-only navigation
- Browser zoom (up to 200%)

## Performance

Optimizations:

- Code splitting per route
- Lazy loading images
- Minified CSS and JS
- Gzip compression
- Service worker caching (PWA)
- Efficient re-renders (React.memo, useCallback)

## Privacy

**Zero tracking guarantee:**

- No Google Analytics or similar tools
- No cookies (except essential session)
- No fingerprinting
- No user profiling
- No data collection
- No third-party scripts

## License

Copyright (C) 2024 Talk-Less Contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

See the LICENSE file in the project root for full license text.

## Contributing

See CONTRIBUTING.md in the project root for guidelines.

## Support

- GitHub Issues: Report bugs or request features
- Documentation: See `/about` and `/transparency` pages
- Source Code: https://github.com/yourusername/Talk-Less
