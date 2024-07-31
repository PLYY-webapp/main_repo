function tag(generate, update) {
    dt = new Date();
    generate.split(' ')[0].split('-')[2]
    update.split(' ')[0].split('-')[2]
    if (generate === update && (generate - dt.getDate()) < 32) {
        return 'new'
    } else if ((update.getDate() - dt.getDate()) < 32) {
        return 'update'
    }
}