# Frontend Rules (frontend/)

## Code Style
- TypeScript strict mode is on — no `any`, no `as unknown as X` casts without a comment explaining why
- Prefer named exports over default exports for components
- Component files: PascalCase (`UserCard.tsx`); utilities: camelCase (`formatDate.ts`)

## React Patterns
- Functional components only — no class components
- Co-locate state with the component that owns it; lift only when two siblings need it
- Custom hooks go in `frontend/src/hooks/` with the `use` prefix

## State Management
- Use React Query for server state (fetching, caching, mutations)
- Use `useState` / `useReducer` for local UI state
- Avoid global state stores unless explicitly needed

## Styling
- Tailwind utility classes only — no inline `style={{}}` except for dynamic values (e.g. computed widths)
- Never write custom CSS files unless Tailwind cannot express the style

## Testing
- Component tests use Vitest + React Testing Library
- Test user behavior, not implementation details (query by role/label, not by class name)
- Every new component needs at least a smoke-test render check
