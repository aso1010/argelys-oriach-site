const CANONICAL_HOST = 'angelventures.biz';

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname === 'gothamgay.com' || url.hostname === 'www.gothamgay.com') {
      if (url.pathname === '/' || url.pathname === '/index.html') {
        const asset = new URL(request.url);
        asset.pathname = '/gotham/';
        return env.ASSETS.fetch(new Request(asset, request));
      }
      return new Response('Not found', { status: 404, headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
    }

    if (url.pathname === '/schema/biography.json') return Response.redirect('https://theangel.biz/schema/biography.json', 301);
    if (url.pathname === '/intake' || url.pathname === '/intake/') {
      return Response.redirect('https://angelventures.biz/' + url.search + '#intake', 301);
    }
    const personal = { '/about': 'bio', '/about/': 'bio' };
    if (personal[url.pathname]) {
      const destination = new URL('https://theangel.biz/');
      destination.search = url.search;
      destination.hash = personal[url.pathname];
      return new Response(null, { status: 301, headers: { Location: destination.href } });
    }
    if (url.pathname === '/practice' || url.pathname === '/practice/') {
      return new Response(null, { status: 301, headers: { Location: 'https://angelventures.biz/#portfolio' } });
    }

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
