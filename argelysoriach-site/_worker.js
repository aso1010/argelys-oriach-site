const CANONICAL_HOST = 'argelysoriach.com';

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const brokenPath = url.pathname === '/beauty-supply';

    if (url.protocol !== 'https:' || url.host !== CANONICAL_HOST || brokenPath) {
      url.protocol = 'https:';
      url.host = CANONICAL_HOST;
      if (brokenPath) url.pathname = '/beauty-salon/';
      return new Response(null, {
        status: 301,
        headers: { Location: url.href },
      });
    }

    return env.ASSETS.fetch(request);
  },
};
