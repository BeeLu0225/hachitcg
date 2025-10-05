// vite.config.js

import { defineConfig } from "vite";
import { ViteEjsPlugin } from "vite-plugin-ejs";
import { fileURLToPath } from "node:url";
import path from "node:path"; // 確保只匯入一次
import { glob } from "glob";

import liveReload from "vite-plugin-live-reload";

function moveOutputPlugin() {
  return {
    name: "move-output",
    enforce: "post",
    apply: "build",
    async generateBundle(options, bundle) {
      for (const fileName in bundle) {
        if (fileName.startsWith("pages/")) {
          const newFileName = fileName.slice("pages/".length);
          bundle[fileName].fileName = newFileName;
        }
      }
    },
  };
}

export default defineConfig({
  // base 的寫法:
  // base: '/Repository 的名稱/'
  base: "/web-layout-training-vite/",
  plugins: [
    liveReload(["./layout/**/*.ejs", "./pages/**/*.ejs", "./pages/**/*.html"]),
    ViteEjsPlugin(),
    moveOutputPlugin(),
  ],
  // -----------------------------
  server: {
    // 啟動 server 時預設開啟的頁面
    open: "pages/index.html",
  },
  // -----------------------------
  // 將 css 設定合併到這裡
  css: {
    preprocessorOptions: {
      scss: {
        // 設定 Sass 的尋找路徑
        includePaths: [path.resolve(__dirname, "node_modules")],
        quietDeps: true // 靜音來自相依套件的警告訊息
      },
    },
  },
  build: {
    rollupOptions: {
      input: Object.fromEntries(
        glob
          .sync("pages/**/*.html")
          .map((file) => [
            path.relative(
              "pages",
              file.slice(0, file.length - path.extname(file).length)
            ),
            fileURLToPath(new URL(file, import.meta.url)),
          ])
      ),
    },
    outDir: "dist",
  },
});
