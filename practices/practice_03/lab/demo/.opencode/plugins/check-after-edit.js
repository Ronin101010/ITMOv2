// OpenCode 2 plugin: run checks after edit and report back
// Minimal example: executes scripts/check.sh and returns output

export default function setup(ctx) {
  ctx.tool.hook("execute.after", async ({ files, result }) => {
    try {
      const run = await ctx.proc.exec({
        cmd: "sh",
        args: ["scripts/check.sh"],
        cwd: ctx.project.root,
      });
      return {
        status: "ok",
        message: `check-after-edit: PASS\n${run.stdout}`,
      };
    } catch (err) {
      // return failure with stderr/stdout if available
      return {
        status: "error",
        message: `check-after-edit: FAIL\n${err?.stderr || err?.message || String(err)}`,
      };
    }
  });
}
