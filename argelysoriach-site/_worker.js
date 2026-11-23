const CANONICAL_HOST = 'angelventures.biz';

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/biography' || url.pathname.startsWith('/biography/')) {
      const destination = new URL('https://theangel.biz/');
      destination.search = url.search;
      destination.hash = 'bio';
      return new Response(null, { status: 301, headers: { Location: destination.href } });
    }

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
