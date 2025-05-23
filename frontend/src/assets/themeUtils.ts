import {
  argbFromHex, 
  themeFromSourceColor,
  applyTheme
} from '@material/material-color-utilities';

/**
 * 应用 Material Design 主题
 * @param sourceColorHex 源颜色的十六进制值（如 '#1976d2'）
 * @param isDark 是否为暗色模式
 */
export function applyMaterialTheme(sourceColorHex = '#1976d2', isDark = false) {
  // 从十六进制颜色转换为 ARGB
  const sourceColor = argbFromHex(sourceColorHex);
  
  // 从源颜色生成主题
  const theme = themeFromSourceColor(sourceColor);
  
  // 应用主题到文档根节点
  applyTheme(theme, {
    target: document.documentElement,
    dark: isDark
  });
}