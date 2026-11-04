function qualityFor(parameters) {
  const quality = parameters.find((parameter) =>
    parameter.trim().toLowerCase().startsWith("q="),
  );
  if (!quality) {
    return 1;
  }

  const value = Number(quality.trim().slice(2));
  return Number.isFinite(value) && value >= 0 && value <= 1 ? value : 0;
}

function prefersMarkdown(request) {
  const accept = request.headers.get("Accept") || "";
  let markdownQuality = 0;
  let htmlQuality = 0;

  for (const entry of accept.split(",")) {
    const [mediaType, ...parameters] = entry.split(";");
    const type = mediaType.trim().toLowerCase();
    if (type === "text/markdown") {
      markdownQuality = Math.max(markdownQuality, qualityFor(parameters));
    } else if (type === "text/html") {
      htmlQuality = Math.max(htmlQuality, qualityFor(parameters));
    }
  }

  return markdownQuality > 0 && markdownQuality >= htmlQuality;
}

function markdownPath(pathname) {
  if (pathname.endsWith(".md")) {
    return null;
  }

  const normalizedPath = pathname.replace(/\/+$/, "");
  if (!normalizedPath) {
    return "/index.md";
  }

  if (normalizedPath.endsWith("/index.html")) {
    return normalizedPath.replace(/index\.html$/, "index.md");
  }

  if (/\.[^/]+$/.test(normalizedPath)) {
    return null;
  }

  return `${normalizedPath}/index.md`;
}

function isContentType(response, type) {
  return (response.headers.get("Content-Type") || "")
    .toLowerCase()
    .startsWith(type);
}

function varyByAccept(response) {
  const headers = new Headers(response.headers);
  const vary = headers.get("Vary");

  if (!vary || vary === "*") {
    headers.set("Vary", vary || "Accept");
  } else if (!vary.split(",").some((value) => value.trim().toLowerCase() === "accept")) {
    headers.set("Vary", `${vary}, Accept`);
  }

  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
}

export default {
  async fetch(request, env) {
    const methodSupportsNegotiation =
      request.method === "GET" || request.method === "HEAD";
    const alternatePath = methodSupportsNegotiation
      ? markdownPath(new URL(request.url).pathname)
      : null;
    const targetPath = alternatePath && prefersMarkdown(request)
      ? alternatePath
      : null;

    if (targetPath) {
      const targetUrl = new URL(request.url);
      targetUrl.pathname = targetPath;
      const markdownRequest = new Request(targetUrl, request);
      const markdownResponse = await env.ASSETS.fetch(markdownRequest);

      if (markdownResponse.ok && isContentType(markdownResponse, "text/markdown")) {
        return varyByAccept(markdownResponse);
      }
    }

    const response = await env.ASSETS.fetch(request);
    const isRedirect = response.status >= 300 && response.status < 400;
    if (
      methodSupportsNegotiation &&
      (isContentType(response, "text/html") || (alternatePath && isRedirect))
    ) {
      return varyByAccept(response);
    }

    return response;
  },
};
