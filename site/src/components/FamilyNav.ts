export function renderFamily(): void {
  const el = document.getElementById("family")
  if (!el) return
  el.innerHTML = `<section><a href="themes/windows/README.md">Windows 主题</a> <a href="themes/terminal/README.md">终端</a> <a href="emotes/README.md">表情</a></section><footer>致谢: 泽央 zeyang / 防御老猫 / 超能尼尔尼尔 (B站 UP)</footer>`
}
