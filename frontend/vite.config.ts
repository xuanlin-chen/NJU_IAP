import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import vueDevTools from "vite-plugin-vue-devtools";

export default defineConfig({
	base: './',
	plugins: [vue(), vueDevTools()],
	resolve: {
		alias: {
			"@": fileURLToPath(new URL("./src", import.meta.url)),
		},
	},
	server: {
		proxy: {
			"/api": {
				target: "http://localhost:5000",
				changeOrigin: true,
			},
		},
	},
	build: {
		chunkSizeWarningLimit: 700,
		assetsDir: 'assets',
		sourcemap: true,
		minify: 'terser',
		terserOptions: {
			compress: {
				drop_console: false,
			},
		},
		rollupOptions: {
			output: {
				assetFileNames: 'assets/[name]-[hash][extname]',
				chunkFileNames: 'assets/[name]-[hash].js',
				entryFileNames: 'assets/[name]-[hash].js',
				manualChunks: (id) => {
					// Create a chunk for core libraries
					if (id.includes('node_modules/vue/') || 
						id.includes('node_modules/vue-router/') || 
						id.includes('node_modules/pinia/')) {
						return 'vendor-core';
					}
					
					// Split naive-ui into smaller chunks
					if (id.includes('node_modules/naive-ui/')) {
						if (id.includes('es/components/button') ||
							id.includes('es/components/space') ||
							id.includes('es/components/config-provider') ||
							id.includes('es/components/message')) {
							return 'naive-ui-basic';
						}
						if (id.includes('es/components/grid') ||
							id.includes('es/components/layout') ||
							id.includes('es/components/modal')) {
							return 'naive-ui-layout';
						}
						if (id.includes('es/components/data-table') ||
							id.includes('es/components/input') ||
							id.includes('es/components/form')) {
							return 'naive-ui-form';
						}
						return 'naive-ui-other';
					}
					
					// Create chunks for icon libraries
					if (id.includes('node_modules/@vicons/')) {
						return 'icons';
					}

					// CSS files
					if (id.includes('.css') || id.includes('style')) {
						return 'styles';
					}

					// Component chunks by feature
					if (id.includes('/src/views/DashboardView/')) {
						return 'dashboard';
					}
					
					if (id.includes('/src/views/ChatView') || 
						id.includes('/components/chat/')) {
						return 'chat';
					}
				}
			},
		},
	},
});
