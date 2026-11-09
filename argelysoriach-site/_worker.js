const CANONICAL_HOST = 'argelysoriach.com';

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const redirectPath = url.pathname === '/beauty-supply'
      ? '/beauty-salon/'
      : url.pathname === '/home' ? '/' : null;

    if (url.protocol !== 'https:' || url.host !== CANONICAL_HOST || redirectPath !== null) {
      url.protocol = 'https:';
      url.host = CANONICAL_HOST;
      if (redirectPath !== null) url.pathname = redirectPath;
      return new Response(null, {
        status: 301,
        headers: { Location: url.href },
      });
    }

    return env.ASSETS.fetch(request);
  },
};
