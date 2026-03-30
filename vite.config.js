import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

/**
 * Local API: `.env.development` に VITE_API_URL=http://127.0.0.1:3000 を書き、
 * 別ターミナルで `npm run api:dev` を実行。
 */
export default defineConfig({
  plugins: [react()],
});
